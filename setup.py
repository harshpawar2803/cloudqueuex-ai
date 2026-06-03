#!/usr/bin/env python3
"""
CloudQueueX AI - DynamoDB Table Setup Script
Creates necessary DynamoDB tables if they don't exist
"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def create_tickets_table():
    """Create Tickets table in DynamoDB"""
    
    try:
        # Check if table exists
        response = dynamodb.describe_table(TableName='Tickets')
        print("✅ Tickets table already exists!")
        return True
    
    except dynamodb.exceptions.ResourceNotFoundException:
        print("📊 Creating Tickets table...")
        
        try:
            dynamodb.create_table(
                TableName='Tickets',
                KeySchema=[
                    {'AttributeName': 'ticket_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'ticket_id', 'AttributeType': 'S'},
                    {'AttributeName': 'timestamp', 'AttributeType': 'S'},
                    {'AttributeName': 'status', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST',
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'StatusIndex',
                        'KeySchema': [
                            {'AttributeName': 'status', 'KeyType': 'HASH'},
                            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'}
                    }
                ],
                Tags=[
                    {'Key': 'Project', 'Value': 'CloudQueueX-AI'},
                    {'Key': 'Environment', 'Value': 'Development'}
                ]
            )
            
            print("✅ Tickets table created successfully!")
            print("📝 Table attributes:")
            print("  - ticket_id (Primary Key)")
            print("  - name, email, team, subject, issue")
            print("  - timestamp, status, ai_analysis")
            return True
        
        except Exception as e:
            print(f"❌ Error creating table: {str(e)}")
            return False
    
    except Exception as e:
        print(f"❌ Error checking table: {str(e)}")
        return False

if __name__ == '__main__':
    print("====================================")
    print("🚀 CloudQueueX AI - Setup Script")
    print("====================================\n")
    
    if create_tickets_table():
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed!")
