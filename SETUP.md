# CloudQueueX AI - Setup Instructions

## Prerequisites
- Python 3.8+
- AWS Account with appropriate permissions
- AWS CLI configured

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file with your AWS credentials:
```
QUEUE_URL=https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT_ID/ticket-queue
TOPIC_ARN=arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:ticket-alert-topic
FLASK_ENV=development
FLASK_DEBUG=False
```

### 3. Setup DynamoDB Table
```bash
python setup.py
```

### 4. Run Flask Application
```bash
python app.py
```

The application will be available at: http://localhost:5000

### 5. Run Worker (in separate terminal)
```bash
python worker.py
```

## Login Credentials
- **Username**: admin | **Password**: CloudQueueX@123 | **Role**: admin
- **Username**: engineer | **Password**: CloudQueueX@123 | **Role**: engineer

## AWS Services Used
- EC2 (Flask Application)
- SQS (Ticket Queue)
- DynamoDB (Ticket Storage)
- SNS (Email Notifications)
- IAM (Permissions)

## Features
✅ Ticket Creation Portal
✅ AI-Powered Ticket Analysis
✅ Queue-Based Processing
✅ Database Storage
✅ Email Notifications
✅ Dashboard with Monitoring
✅ Ticket Search & Tracking
