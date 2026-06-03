import boto3
import json
import time
import uuid

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

    issue_lower = issue.lower()

    category = "General"
    priority = "Medium"
    recommended_team = "Support"

    if any(word in issue_lower for word in
           ["server", "linux", "disk", "cpu", "memory", "ec2"]):

        category = "Infrastructure"
        priority = "High"
        recommended_team = "Infrastructure"

    elif any(word in issue_lower for word in
             ["network", "dns", "vpn", "latency"]):

        category = "Networking"
        priority = "High"
        recommended_team = "Networking"

    elif any(word in issue_lower for word in
             ["jenkins", "pipeline", "docker",
              "kubernetes", "deployment", "cicd"]):

        category = "DevOps"
        priority = "High"
        recommended_team = "DevOps"

    elif any(word in issue_lower for word in
             ["security", "iam", "access", "authentication"]):

        category = "Security"
        priority = "Critical"
        recommended_team = "Security"

    summary = issue[:150]

    return f"""
Category: {category}

Priority: {priority}

Recommended Team: {recommended_team}

Summary: {summary}
"""

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

            ticket_id = body.get('ticket_id', str(uuid.uuid4()))
            name = body.get('name', 'Unknown')
            email = body.get('email', 'N/A')
            team = body.get('team', 'General')
            subject = body.get('subject', 'No Subject')
            issue = body.get('issue', 'No Issue Provided')
            timestamp = body.get('timestamp', 'N/A')

            print("\n====================================")
            print("🎫 NEW SUPPORT TICKET")
            print("====================================")

            print("Ticket ID :", ticket_id)
            print("Name      :", name)
            print("Email     :", email)
            print("Team      :", team)
            print("Subject   :", subject)
            print("Timestamp :", timestamp)

            print("\n📝 Issue Description")
            print("------------------------------------")
            print(issue)

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
                    'subject': subject,
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

                Subject='CloudQueueX AI - New Ticket Created',

                Message=f"""

CloudQueueX AI Notification

====================================

New Support Ticket Received

Ticket ID : {ticket_id}
Name      : {name}
Email     : {email}
Team      : {team}
Subject   : {subject}
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