<p align="center">
  <img src="./images/images/mainmeduim.png" alt="AWS AI Portfolio Chatbot Architecture" width="100%">
</p>

# 🚀 AWS AI Portfolio Chatbot

A serverless AI-powered portfolio chatbot built using AWS, Terraform, OpenAI, and modern cloud engineering practices.

### Built With

Terraform • AWS Lambda • API Gateway • DynamoDB • S3 • Secrets Manager • CloudWatch • OpenAI

🌐 Live Demo: https://ashleyschippers.dev

📝 Article: https://medium.com/@ashley.schippersas/building-my-aws-ai-portfolio-chatbot-with-terraform-lambda-and-openai-95730daec82c

![Terraform](https://img.shields.io/badge/Terraform-IaC-623CE4)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900)
![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-4053D6)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-10A37F)
![Python](https://img.shields.io/badge/Python-3.12-blue)

## 🎯 Project Goal

The goal of this project was to build a production-style serverless AI chatbot capable of answering questions about a portfolio website while demonstrating practical cloud engineering skills.

The chatbot includes:

- Infrastructure as Code with Terraform
- AWS Serverless Architecture
- OpenAI Integration
- Secure Secrets Management
- Rate Limiting and Cost Controls
- Portfolio Knowledge Stored in S3
- Monitoring and Logging with CloudWatch

This project was built as part of my cloud engineering learning journey and serves as a real-world portfolio application.

## 📸 



![](./images/images/aws-ai-chatbot-architecture.png)


## 🏗 Architecture

The chatbot follows a fully serverless architecture:

Portfolio Website → API Gateway → AWS Lambda → OpenAI API

Supporting services:

- DynamoDB (chat history & rate limiting)
- S3 (portfolio knowledge base)
- Secrets Manager (API key storage)
- CloudWatch (logging & monitoring)

## 📚 Lessons Learned

During this project I gained hands-on experience with:

- Terraform workflows
- IAM permissions
- Lambda troubleshooting
- API Gateway integrations
- DynamoDB design
- Secrets Manager
- CloudWatch debugging
- Rate limiting strategies
- Production deployment workflows

The biggest lesson was learning how to troubleshoot cloud systems by reading logs, identifying root causes, and resolving issues step by step.

## 💰 Cost Optimisation

This architecture was designed to be affordable for personal portfolio use.

Features include:

- Serverless infrastructure
- DynamoDB TTL cleanup
- Session limits
- Per-minute rate limits
- Per-day rate limits
- Secure API key storage

Typical monthly AWS costs are minimal for low-traffic personal projects, with OpenAI usage being the primary variable cost.

## 🌐 Connect

Portfolio: https://ashleyschippers.dev

LinkedIn: https://www.linkedin.com/in/ashley-schippers-90a37084/

Medium: https://medium.com/@ashley.schippersas

GitHub: https://github.com/Ashnetnase

