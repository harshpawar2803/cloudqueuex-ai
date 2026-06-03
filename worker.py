#!/usr/bin/env python3
"""
CloudQueueX AI - Background Worker Service
Processes tickets from SQS queue, stores in DynamoDB, sends SNS notifications
"""

import boto3
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# =========================================
# AWS CLIENT INITIALIZATION
# =========================================

sqs = boto3.client('sqs', region_name='us-east-1')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

sns = boto3.client('sns', region_name='us-east-1')

# =========================================
# ENVIRONMENT VARIABLES
# =========================================

QUEUE_URL = os.environ.get('QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/686849057833/ticket-queue')

TOPIC_ARN = os.environ.get('TOPIC_ARN', 'arn:aws:sns:us-east-1:686849057833:ticket-alert-topic')

# =========================================
# WORKER FUNCTION
# =========================================

def process_ticket(message_body):

    """Process a ticket message from SQS"""

    try:
        ticket_data = json.loads(message_body)

        ticket_id = ticket_data.get('ticket_id')

        name = ticket_data.get('name')

        email = ticket_data.get('email')

        team = ticket_data.get('team')

        subject = ticket_data.get('subject')

        issue = ticket_data.get('issue')

        timestamp = ticket_data.get('timestamp')

        print(f"Processing ticket: {ticket_id}")

        # ===== STORE IN DYNAMODB =====

        table = dynamodb.Table('Tickets')

        ai_analysis = f"Ticket from {name} in {team} team regarding: {subject}"

        try:
            table.put_item(

                Item={

                    'ticket_id': ticket_id,

                    'name': name,

                    'email': email,

                    'team': team,

                    'subject': subject,

                    'issue': issue,

                    'timestamp': timestamp,

                    'status': 'OPEN',

                    'ai_analysis': ai_analysis

                }

            )

            print(f"✅ Ticket stored in DynamoDB: {ticket_id}")

        except Exception as e:
            print(f"❌ DynamoDB Error: {str(e)}")
            raise

        # ===== SEND EMAIL NOTIFICATION =====

        try:
            sns.publish(

                TopicArn=TOPIC_ARN,

                Subject=f"New Support Ticket: {subject}",

                Message=f"""
New ticket received from {name}:

Team: {team}
Subject: {subject}
Status: OPEN
Ticket ID: {ticket_id}

Issue Details:
{issue}

AI Analysis:
{ai_analysis}

Click to view ticket details.
                """

            )

            print(f"✅ Email notification sent: {email}")

        except Exception as e:
            print(f"❌ SNS Error: {str(e)}")
            raise

    except Exception as e:
        print(f"❌ Error processing ticket: {str(e)}")
        raise


def main_worker_loop():

    """Main worker loop - continuously poll SQS"""

    print("====================================")
    print("🚀 CloudQueueX AI Worker Started")
    print("====================================")

    print(f"Queue URL: {QUEUE_URL}")

    print(f"Topic ARN: {TOPIC_ARN}\n")

    while True:

        try:
            # RECEIVE MESSAGES FROM SQS

            response = sqs.receive_message(

                QueueUrl=QUEUE_URL,

                MaxNumberOfMessages=10,

                WaitTimeSeconds=20

            )

            # ===== PROCESS MESSAGES =====

            if 'Messages' in response:

                for message in response['Messages']:

                    try:
                        # PROCESS TICKET

                        process_ticket(message['Body'])

                        # DELETE MESSAGE FROM QUEUE

                        try:
                            sqs.delete_message(

                                QueueUrl=QUEUE_URL,

                                ReceiptHandle=message['ReceiptHandle']

                            )

                            print(f"✅ Message deleted from queue\n")

                        except Exception as e:
                            print(f"❌ Error deleting message: {str(e)}\n")

                    except Exception as e:
                        print(f"❌ Error processing message: {str(e)}\n")
                        # Message will return to queue after visibility timeout

            else:

                print("No messages in queue, waiting...\n")

        except Exception as e:
            print(f"❌ Error in main loop: {str(e)}")
            print("Retrying in 10 seconds...\n")
            time.sleep(10)


# =========================================
# RUN WORKER
# =========================================

if __name__ == '__main__':

    main_worker_loop()
