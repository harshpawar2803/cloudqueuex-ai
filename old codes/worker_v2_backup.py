import boto3
import json
import time
import uuid
import openai

# =========================================
# OPENAI API CONFIGURATION
# =========================================

openai.api_key = ""

# =========================================
# AWS CLIENTS
# =========================================

sqs = boto3.client('sqs', region_name='us-east-1')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

sns = boto3.client('sns', region_name='us-east-1')

# =========================================
# DYNAMODB TABLE
# =========================================

table = dynamodb.Table('Tickets')

# =========================================
# SQS QUEUE URL
# =========================================

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/686849057833/ticket-queue'

# =========================================
# SNS TOPIC ARN
# =========================================

TOPIC_ARN = 'arn:aws:sns:us-east-1:686849057833:ticket-alert-topic'

# =========================================
# AI ANALYSIS FUNCTION
# =========================================

def analyze_ticket(issue):

    try:

        response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo",

            messages=[

                {
                    "role": "system",

                    "content": """

You are an intelligent AI support assistant.

Analyze support tickets and provide:

1. Ticket Category
2. Priority Level
3. Recommended Support Team
4. Short Summary

Return response in clean professional format.

"""
                },

                {
                    "role": "user",
                    "content": issue
                }

            ]

        )

        return response['choices'][0]['message']['content']

    except Exception as e:

        return f"AI Analysis Failed: {str(e)}"

# =========================================
# WORKER START
# =========================================

print("====================================")
print("🚀 CloudQueueX AI Worker Started")
print("====================================")

# =========================================
# MAIN LOOP
# =========================================

while True:

    response = sqs.receive_message(

        QueueUrl=QUEUE_URL,

        MaxNumberOfMessages=1,

        WaitTimeSeconds=5

    )

    messages = response.get('Messages', [])

    if messages:

        for message in messages:

            body = json.loads(message['Body'])

            # =========================================
            # TICKET DETAILS
            # =========================================

            ticket_id = body.get('ticket_id', str(uuid.uuid4()))

            name = body.get('name', 'Unknown')

            email = body.get('email', 'N/A')

            team = body.get('team', 'General')

            issue = body.get('issue', 'No Issue Provided')

            timestamp = body.get('timestamp', 'N/A')

            print("\n====================================")
            print("🎫 NEW SUPPORT TICKET")
            print("====================================")

            print("Ticket ID :", ticket_id)
            print("Name      :", name)
            print("Email     :", email)
            print("Team      :", team)
            print("Timestamp :", timestamp)

            print("\n📝 Issue Description")
            print("------------------------------------")
            print(issue)

            # =========================================
            # OPENAI ANALYSIS
            # =========================================

            print("\n🤖 Running AI Analysis...")

            ai_result = analyze_ticket(issue)

            print("\n====================================")
            print("🤖 AI ANALYSIS RESULT")
            print("====================================")

            print(ai_result)

            # =========================================
            # STORE IN DYNAMODB
            # =========================================

            table.put_item(

                Item={

                    'ticket_id': ticket_id,

                    'name': name,

                    'email': email,

                    'team': team,

                    'issue': issue,

                    'timestamp': timestamp,

                    'status': 'OPEN',

                    'ai_analysis': ai_result

                }

            )

            print("\n✅ Ticket Stored in DynamoDB")

            # =========================================
            # SNS EMAIL ALERT
            # =========================================

            sns.publish(

                TopicArn=TOPIC_ARN,

                Subject='🚀 CloudQueueX AI - New Ticket Created',

                Message=f"""

CloudQueueX AI Notification

====================================

New Support Ticket Received

Ticket ID : {ticket_id}

Name      : {name}

Email     : {email}

Team      : {team}

Timestamp : {timestamp}

====================================

Issue Description

{issue}

====================================

AI Analysis

{ai_result}

====================================

AWS Event-Driven Ticket Processing Platform

"""

            )

            print("📧 SNS Email Notification Sent")

            # =========================================
            # DELETE MESSAGE FROM SQS
            # =========================================

            sqs.delete_message(

                QueueUrl=QUEUE_URL,

                ReceiptHandle=message['ReceiptHandle']

            )

            print("🗑 Message Deleted From SQS")

            print("====================================")

    else:

        print("⏳ Waiting for new support tickets...")

    time.sleep(5)
