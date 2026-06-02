import boto3
import json
import time
import uuid

# =========================================
# AWS CLIENTS
# =========================================

sqs = boto3.client(
    'sqs',
    region_name='us-east-1'
)

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1'
)

sns = boto3.client(
    'sns',
    region_name='us-east-1'
)

# =========================================
# DYNAMODB TABLE
# =========================================

table = dynamodb.Table('Tickets')

# =========================================
# SQS QUEUE URL
# =========================================

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/686849057833/ticket-queue"

# =========================================
# SNS TOPIC ARN
# =========================================

TOPIC_ARN = "arn:aws:sns:us-east-1:686849057833:ticket-alert-topic"

# =========================================
# AI ANALYSIS ENGINE
# =========================================

def analyze_ticket(issue):

    issue = issue.lower()

    # Infrastructure

    if (
        "server" in issue
        or "linux" in issue
        or "cpu" in issue
        or "disk" in issue
        or "storage" in issue
    ):
        return {
            "category": "Infrastructure",
            "priority": "HIGH",
            "summary": "Server or infrastructure issue detected",
            "assigned_team": "Cloud Operations"
        }

    # Networking

    elif (
        "network" in issue
        or "latency" in issue
        or "connection" in issue
        or "vpn" in issue
    ):
        return {
            "category": "Networking",
            "priority": "HIGH",
            "summary": "Network connectivity issue detected",
            "assigned_team": "Network Team"
        }

    # Access Management

    elif (
        "password" in issue
        or "login" in issue
        or "access" in issue
        or "permission" in issue
    ):
        return {
            "category": "Access Management",
            "priority": "MEDIUM",
            "summary": "User access related issue",
            "assigned_team": "IAM Team"
        }

    # Billing

    elif (
        "payment" in issue
        or "billing" in issue
        or "invoice" in issue
    ):
        return {
            "category": "Billing",
            "priority": "MEDIUM",
            "summary": "Billing related request",
            "assigned_team": "Finance Team"
        }

    # Default

    else:
        return {
            "category": "General",
            "priority": "LOW",
            "summary": "General support request",
            "assigned_team": "Support Team"
        }

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

    messages = response.get("Messages", [])

    if messages:

        for message in messages:

            body = json.loads(message["Body"])

            ticket_id = body.get(
                "ticket_id",
                str(uuid.uuid4())
            )

            name = body.get(
                "name",
                "Unknown"
            )

            email = body.get(
                "email",
                "N/A"
            )

            team = body.get(
                "team",
                "General"
            )

            subject = body.get(
                "subject",
                "No Subject"
            )

            issue = body.get(
                "issue",
                "No Issue Provided"
            )

            timestamp = body.get(
                "timestamp",
                "N/A"
            )

            print("\n====================================")
            print("🎫 NEW SUPPORT TICKET")
            print("====================================")

            print("Ticket ID :", ticket_id)
            print("Name      :", name)
            print("Email     :", email)
            print("Team      :", team)
            print("Timestamp :", timestamp)

            print("\n📝 Issue")
            print("------------------------------------")
            print(issue)

            # =====================================
            # AI ANALYSIS
            # =====================================

            analysis = analyze_ticket(issue)

            print("\n🤖 AI ANALYSIS")
            print("------------------------------------")

            print("Category :", analysis["category"])
            print("Priority :", analysis["priority"])
            print("Summary  :", analysis["summary"])
            print("Assigned :", analysis["assigned_team"])

            # =====================================
            # DYNAMODB STORE
            # =====================================

            table.put_item(
                Item={
                    "ticket_id": ticket_id,
                    "name": name,
                    "email": email,
                    "team": team,
                    "subject": subject,
                    "issue": issue,
                    "timestamp": timestamp,

                    "status": "OPEN",

                    "category": analysis["category"],
                    "priority": analysis["priority"],
                    "summary": analysis["summary"],
                    "assigned_team": analysis["assigned_team"]
                }
            )

            print("\n✅ Stored In DynamoDB")

            # =====================================
            # SNS ALERT
            # =====================================

            sns.publish(
                TopicArn=TOPIC_ARN,
                Subject="CloudQueueX AI - New Ticket",

                Message=f"""

CloudQueueX AI Notification

====================================

Ticket ID : {ticket_id}

Name : {name}

Email : {email}

Team : {team}

Subject : {subject}

Timestamp : {timestamp}

====================================

Issue

{issue}

====================================

Category : {analysis['category']}

Priority : {analysis['priority']}

Summary : {analysis['summary']}

Assigned Team : {analysis['assigned_team']}

Status : OPEN

====================================

AWS Event Driven Ticket Platform

"""
            )

            print("📧 SNS Notification Sent")

            # =====================================
            # DELETE SQS MESSAGE
            # =====================================

            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"]
            )

            print("🗑 Message Deleted From SQS")
            print("====================================")

    else:

        print("⏳ Waiting for tickets...")

    time.sleep(5)