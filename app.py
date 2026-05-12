from flask import Flask, request, render_template_string
import boto3
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# =========================================
# AWS SQS CONFIGURATION
# =========================================

sqs = boto3.client('sqs', region_name='us-east-1')

QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/686849057833/ticket-queue'

# =========================================
# MAIN DASHBOARD UI
# =========================================

html = """

<!DOCTYPE html>
<html>

<head>

    <title>CloudQueueX AI</title>

    <meta charset="UTF-8">

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
        }

        body{
            font-family:Arial,sans-serif;
            background:#0f172a;
            color:white;
        }

        /* NAVBAR */

        .navbar{

            display:flex;
            justify-content:space-between;
            align-items:center;

            padding:20px 60px;

            background:#111827;

            border-bottom:1px solid #1f2937;

        }

        .logo{

            font-size:30px;
            font-weight:bold;
            color:#38bdf8;

        }

        .logo span{
            color:white;
        }

        .nav-links a{

            color:#d1d5db;
            text-decoration:none;
            margin-left:25px;
            font-size:15px;

        }

        .nav-links a:hover{
            color:#38bdf8;
        }

        /* HERO */

        .hero{

            text-align:center;
            padding:70px 20px 30px;

        }

        .badge{

            display:inline-block;

            background:#1e293b;

            color:#38bdf8;

            padding:8px 18px;

            border-radius:30px;

            border:1px solid #334155;

            margin-bottom:25px;

        }

        .hero h1{

            font-size:58px;
            margin-bottom:18px;

        }

        .hero p{

            color:#cbd5e1;

            font-size:18px;

            line-height:1.8;

        }

        /* MAIN CARD */

        .container{

            width:100%;

            display:flex;

            justify-content:center;

            margin-top:40px;

        }

        .card{

            width:600px;

            background:#111827;

            padding:40px;

            border-radius:20px;

            border:1px solid #1f2937;

            box-shadow:0 0 30px rgba(0,0,0,0.5);

        }

        .card h2{

            text-align:center;

            margin-bottom:30px;

            font-size:28px;

        }

        label{

            display:block;

            margin-top:18px;

            margin-bottom:8px;

            color:#cbd5e1;

            font-size:15px;

        }

        input, textarea, select{

            width:100%;

            padding:14px;

            border:none;

            border-radius:10px;

            background:#1e293b;

            color:white;

            font-size:15px;

        }

        textarea{

            height:150px;

            resize:none;

        }

        button{

            width:100%;

            padding:15px;

            margin-top:25px;

            border:none;

            border-radius:12px;

            background:linear-gradient(to right,#0ea5e9,#2563eb);

            color:white;

            font-size:16px;

            font-weight:bold;

            cursor:pointer;

        }

        button:hover{
            opacity:0.92;
        }

        /* STATS */

        .stats{

            display:flex;

            justify-content:center;

            gap:20px;

            margin:60px 20px;

            flex-wrap:wrap;

        }

        .stat-box{

            width:230px;

            background:#111827;

            padding:25px;

            border-radius:18px;

            border:1px solid #1f2937;

            text-align:center;

        }

        .stat-box h2{

            color:#38bdf8;

            margin-bottom:10px;

            font-size:30px;

        }

        .stat-box p{

            color:#cbd5e1;

        }

        /* FEATURES */

        .features{

            display:flex;

            justify-content:center;

            gap:25px;

            margin:40px 20px 70px;

            flex-wrap:wrap;

        }

        .feature-box{

            width:280px;

            background:#111827;

            padding:28px;

            border-radius:18px;

            border:1px solid #1f2937;

        }

        .feature-box h3{

            color:#38bdf8;

            margin-bottom:12px;

        }

        .feature-box p{

            color:#cbd5e1;

            line-height:1.7;

            font-size:14px;

        }

        /* FOOTER */

        .footer{

            text-align:center;

            padding:30px;

            color:#94a3b8;

            border-top:1px solid #1f2937;

        }

    </style>

</head>

<body>

    <!-- NAVBAR -->

    <div class="navbar">

        <div class="logo">
            ☁️ CloudQueue<span>X AI</span>
        </div>

        <div class="nav-links">

            <a href="/">Dashboard</a>

            <a href="/architecture">Architecture</a>

            <a href="/services">AWS Services</a>

            <a href="/support">Support</a>

        </div>

    </div>

    <!-- HERO -->

    <div class="hero">

        <div class="badge">
            AI-Powered Event-Driven Ticket Processing Platform
        </div>

        <h1>CloudQueueX AI</h1>

        <p>
            Modern cloud-native ticket management system powered by AWS,
            asynchronous processing, intelligent workflows, and AI-assisted analysis.
        </p>

    </div>

    <!-- MAIN FORM -->

    <div class="container">

        <div class="card">

            <h2>🎫 Create Support Ticket</h2>

            <form action="/submit" method="POST">

                <label>Full Name</label>

                <input type="text" name="name" placeholder="Enter your full name" required>

                <label>Email Address</label>

                <input type="email" name="email" placeholder="Enter email address" required>

                <label>Support Team</label>

                <select name="team" required>

                    <option value="">Select Team</option>

                    <option>Infrastructure</option>

                    <option>Networking</option>

                    <option>DevOps</option>

                    <option>Security</option>

                    <option>Billing</option>

                </select>

                <label>Ticket Subject</label>

                <input type="text" name="subject" placeholder="Short issue title" required>

                <label>Ticket Description</label>

                <textarea name="issue" placeholder="Describe issue in detail..." required></textarea>

                <button type="submit">
                    🚀 Submit Ticket
                </button>

            </form>

        </div>

    </div>

    <!-- STATS -->

    <div class="stats">

        <div class="stat-box">

            <h2>AWS</h2>

            <p>Cloud-Native Infrastructure</p>

        </div>

        <div class="stat-box">

            <h2>99.9%</h2>

            <p>System Availability</p>

        </div>

        <div class="stat-box">

            <h2>AI</h2>

            <p>Intelligent Ticket Analysis</p>

        </div>

    </div>

    <!-- FEATURES -->

    <div class="features">

        <div class="feature-box">

            <h3>⚡ Event-Driven Architecture</h3>

            <p>
                Uses Amazon SQS for asynchronous queue processing and scalable distributed workflows.
            </p>

        </div>

        <div class="feature-box">

            <h3>🤖 AI-Powered Processing</h3>

            <p>
                Integrates OpenAI-based intelligent ticket analysis, classification, and prioritization.
            </p>

        </div>

        <div class="feature-box">

            <h3>☁️ Cloud-Native Design</h3>

            <p>
                Built using AWS EC2, SQS, DynamoDB, SNS,
                IAM, CloudFormation, and Application Load Balancer.
            </p>

        </div>

    </div>

    <!-- FOOTER -->

    <div class="footer">

        © 2026 CloudQueueX AI • AWS Event-Driven AI Platform

    </div>

</body>

</html>

"""

# =========================================
# HOME PAGE
# =========================================

@app.route('/')
def home():

    return render_template_string(html)

# =========================================
# ARCHITECTURE PAGE
# =========================================

@app.route('/architecture')
def architecture():

    return """

    <body style='background:#0f172a;color:white;font-family:Arial;padding:50px;'>

    <h1>☁️ CloudQueueX AI Architecture</h1>

    <br><br>

    <h2>System Workflow</h2>

    <pre style='font-size:20px;color:#38bdf8;'>

User
 ↓
Application Load Balancer
 ↓
EC2 Flask Frontend
 ↓
Amazon SQS Queue
 ↓
Worker Service
 ↓
OpenAI AI Analysis
 ↓
DynamoDB Storage
 ↓
SNS Email Notifications

    </pre>

    <br><br>

    <h2>AWS Services Used</h2>

    <ul style='line-height:2;font-size:18px;'>

        <li>Amazon EC2</li>

        <li>Amazon SQS</li>

        <li>Amazon DynamoDB</li>

        <li>Amazon SNS</li>

        <li>AWS IAM</li>

        <li>AWS CloudFormation</li>

        <li>Application Load Balancer</li>

        <li>OpenAI API</li>

    </ul>

    <br><br>

    <a href='/' style='color:#38bdf8;font-size:20px;text-decoration:none;'>
        ← Back to Dashboard
    </a>

    </body>

    """

# =========================================
# SERVICES PAGE
# =========================================

@app.route('/services')
def services():

    return """

    <body style='background:#0f172a;color:white;font-family:Arial;padding:50px;'>

    <h1>🚀 AWS Services Used</h1>

    <br><br>

    <table border='1' cellpadding='15'
    style='border-collapse:collapse;font-size:18px;'>

        <tr>
            <th>Service</th>
            <th>Purpose</th>
        </tr>

        <tr>
            <td>EC2</td>
            <td>Hosts Flask frontend application</td>
        </tr>

        <tr>
            <td>SQS</td>
            <td>Asynchronous ticket queue</td>
        </tr>

        <tr>
            <td>DynamoDB</td>
            <td>Stores ticket records</td>
        </tr>

        <tr>
            <td>SNS</td>
            <td>Email notifications</td>
        </tr>

        <tr>
            <td>IAM</td>
            <td>Secure AWS service permissions</td>
        </tr>

        <tr>
            <td>CloudFormation</td>
            <td>Infrastructure as Code</td>
        </tr>

        <tr>
            <td>ALB</td>
            <td>Load balancing and scalability</td>
        </tr>

        <tr>
            <td>OpenAI</td>
            <td>AI-powered ticket analysis</td>
        </tr>

    </table>

    <br><br>

    <a href='/' style='color:#38bdf8;font-size:20px;text-decoration:none;'>
        ← Back to Dashboard
    </a>

    </body>

    """

# =========================================
# SUPPORT PAGE
# =========================================

@app.route('/support')
def support():

    return """

    <body style='background:#0f172a;color:white;font-family:Arial;padding:50px;text-align:center;'>

    <h1>📞 Support Center</h1>

    <br><br>

    <p style='font-size:20px;'>

    CloudQueueX AI is an AI-powered cloud-native ticket processing platform
    designed using AWS event-driven architecture principles.

    </p>

    <br>

    <h2>Project Features</h2>

    <ul style='line-height:2;font-size:18px;list-style:none;'>

        <li>✅ Event-Driven Workflow</li>

        <li>✅ AI Ticket Analysis</li>

        <li>✅ AWS Cloud Infrastructure</li>

        <li>✅ Distributed Queue Processing</li>

        <li>✅ Infrastructure as Code</li>

        <li>✅ Cloud-Native Architecture</li>

    </ul>

    <br><br>

    <a href='/' style='color:#38bdf8;font-size:20px;text-decoration:none;'>
        ← Back to Dashboard
    </a>

    </body>

    """

# =========================================
# SUBMIT ROUTE
# =========================================

@app.route('/submit', methods=['POST'])
def submit():

    ticket_id = str(uuid.uuid4())

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name = request.form['name']

    email = request.form['email']

    team = request.form['team']

    subject = request.form['subject']

    issue = request.form['issue']

    # SEND MESSAGE TO SQS

    sqs.send_message(

        QueueUrl=QUEUE_URL,

        MessageBody=json.dumps({

            'ticket_id': ticket_id,

            'name': name,

            'email': email,

            'team': team,

            'subject': subject,

            'issue': issue,

            'timestamp': timestamp

        })

    )

    return f"""

    <body style="background:#0f172a;color:white;font-family:Arial;text-align:center;padding-top:80px;">

        <h1>✅ Ticket Submitted Successfully</h1>

        <br>

        <h2>🎫 Ticket ID</h2>

        <p style="font-size:24px;color:#38bdf8;">{ticket_id}</p>

        <br>

        <h3>Name: {name}</h3>

        <h3>Email: {email}</h3>

        <h3>Team: {team}</h3>

        <h3>Subject: {subject}</h3>

        <h3>Timestamp: {timestamp}</h3>

        <br>

        <p style="font-size:18px;">
            Ticket successfully pushed to AWS SQS Queue 🚀
        </p>

        <br><br>

        <a href="/" style="color:#38bdf8;font-size:20px;text-decoration:none;">
            ← Back to Dashboard
        </a>

    </body>

    """

# =========================================
# RUN APPLICATION
# =========================================

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
