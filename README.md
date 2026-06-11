# Serverless AI Chatbot on AWS

A public-safe example of a serverless AI chatbot backend built with Terraform, AWS Lambda, API Gateway, DynamoDB, Amazon S3, Secrets Manager, CloudWatch and OpenAI.

## Overview

This project demonstrates how to build a serverless chatbot backend for a professional portfolio website.

The chatbot uses:

- API Gateway to expose a public HTTP endpoint
- Lambda to process chat requests
- OpenAI to generate responses
- S3 to store public portfolio knowledge
- DynamoDB to store chat history and rate-limit counters
- Secrets Manager to store the OpenAI API key securely
- CloudWatch for logs
- Terraform for Infrastructure as Code

## Architecture

```text
Portfolio Website
      ↓
API Gateway
      ↓
AWS Lambda
      ↓
OpenAI API

Additional services:

Lambda → DynamoDB       Chat history, sessions and rate limits
Lambda → S3             Portfolio knowledge JSON
Lambda → Secrets Manager OpenAI API key
Lambda → CloudWatch     Logs and troubleshooting
Features
Infrastructure as Code with Terraform
Serverless backend
OpenAI integration
Portfolio knowledge stored in S3
Chat history in DynamoDB
Session tracking
Per-session message limits
Per-minute and per-day rate limiting
DynamoDB TTL cleanup
CloudWatch logging
Secrets stored in AWS Secrets Manager
Estimated Cost

For low-traffic portfolio use, this architecture is designed to be low cost.

Typical cost drivers:

Secrets Manager has a small monthly cost per secret
OpenAI usage depends on request volume
Lambda, API Gateway, S3 and DynamoDB are usually low cost at small scale
Security Notes

Do not commit:

terraform.tfvars
Terraform state files
API keys
AWS credentials
Secrets
Private infrastructure details

Use terraform.tfvars.example as a safe template.

Setup
Copy the example variable file:
cp terraform.tfvars.example terraform.tfvars
Add your own values:
aws_region            = "ap-southeast-2"
knowledge_bucket_name = "your-unique-chatbot-knowledge-bucket"
allowed_origins       = ["https://your-website.example"]
openai_api_key        = "sk-your-openai-api-key"
Deploy:
terraform init
terraform plan
terraform apply
Test:
curl -X POST "https://your-api-url/chat" \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"demo","message":"Hello"}'
Live Demo

This public template is based on a live portfolio chatbot project.

Blog Article: https://medium.com/@ashley.schippersas/building-my-aws-ai-portfolio-chatbot-with-terraform-lambda-and-openai-95730daec82c

Read the project write-up:

Building My AWS AI Portfolio Chatbot with Terraform, Lambda and OpenAI

License

MIT