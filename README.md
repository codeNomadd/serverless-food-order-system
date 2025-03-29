# 🍽️ Food Delivery REST API

🧠 **Portfolio Project**  
Built to demonstrate real-world AWS DevOps and Cloud Engineering skills.  
Includes observability, security, cost tracking, and system design.

A serverless food ordering system built with AWS Lambda, API Gateway, DynamoDB, and S3. This project demonstrates a modern, scalable architecture for handling food delivery orders with a responsive frontend.

## 📐 Tech Stack

- **Backend**
  - AWS Lambda (Python 3.12)
  - Amazon API Gateway (REST API)
  - Amazon DynamoDB (NoSQL Database)
  - IAM (Security & Permissions)
  - CloudWatch (Monitoring & Alerts)
  - SNS (Notifications)

- **Frontend**
  - HTML5, CSS3, JavaScript
  - Tailwind CSS for styling
  - Axios for API calls
  - SweetAlert2 for enhanced UX

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend      │     │   API        │     │   Lambda     │
│   (S3 Static)   │────▶│   Gateway    │────▶│   Function   │
└─────────────────┘     └──────────────┘     └──────────────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │  DynamoDB    │
                                              │   Table      │
                                              └──────────────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │  CloudWatch  │
                                              │  Monitoring  │
                                              └──────────────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │     SNS      │
                                              │   Alerts     │
                                              └──────────────┘
```

## 🎯 AWS Well-Architected Framework Implementation

This project is designed to demonstrate AWS best practices while maintaining a balance between production readiness and skill demonstration. Here's how we've implemented each pillar:

### 1️⃣ Operational Excellence
- ✅ Structured logging with CloudWatch
- ✅ Comprehensive error handling
- ✅ Infrastructure as Code (SAM template)
- ✅ Detailed documentation and deployment guides
- ✅ Reproducible deployment process

### 2️⃣ Security
- ✅ IAM roles with least privilege access
- ✅ DynamoDB access scoped to specific operations
- ✅ API Gateway with CORS protection
- ✅ Secure S3 bucket configuration
- ✅ Encryption at rest enabled for DynamoDB (SSESpecification)
- ⚠️ Note: WAF and API keys omitted as they're not essential for skill demonstration

### 3️⃣ Reliability
- ✅ DynamoDB auto-scaling (5-20 units)
- ✅ Point-in-Time Recovery (PITR) for backups
- ✅ CloudWatch alarms for errors and throttles
- ✅ SNS notifications for critical events
- ✅ Error retry mechanisms in Lambda
- ⚠️ Note: Multi-region deployment is not implemented, but can be added for high availability in production environments

### 4️⃣ Performance Efficiency
- ✅ Serverless architecture for optimal scaling
- ✅ Connection reuse in Lambda
- ✅ Efficient DynamoDB access patterns
- ⚠️ Note: CloudFront CDN omitted as it's not essential for demonstration

### 5️⃣ Cost Optimization
- ✅ Serverless components to minimize idle costs
- ✅ DynamoDB auto-scaling to prevent overprovisioning
- ✅ CloudWatch log retention (14 days)
- ⚠️ Note: AWS Budgets omitted as they're not essential for demonstration

## 📁 Project Structure

```
food-delivery/
├── backend/                    # Lambda function and IAM policies
│   ├── lambda_function.py     # Lambda handler code
│   └── lambda-policy.json     # IAM permissions for Lambda
├── frontend/                  # Static website files
│   ├── index.html            # Main HTML file
│   ├── styles.css            # CSS styles
│   └── scripts.js            # Frontend JavaScript
├── infra/                    # Infrastructure policies
│   └── trust-policy.json     # IAM trust policy for Lambda
├── template.yaml             # SAM template for IaC
├── s3-bucket-policy.json     # S3 bucket policy
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

## 🚀 Setup & Deployment

### Option 1: SAM Template Deployment (Recommended)
```bash
# Install AWS SAM CLI
brew install aws-sam-cli

# Build and deploy using SAM
sam build
sam deploy --guided

# Follow the prompts to configure your deployment
```

### Option 2: Manual CLI Deployment

```bash
# Create DynamoDB table
aws dynamodb create-table \
    --table-name FoodOrders \
    --attribute-definitions AttributeName=orderId,AttributeType=S \
    --key-schema AttributeName=orderId,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# Create IAM role
aws iam create-role \
    --role-name FoodDeliveryLambdaRole \
    --assume-role-policy-document file://infra/trust-policy.json

# Attach permissions
aws iam put-role-policy \
    --role-name FoodDeliveryLambdaRole \
    --policy-name FoodDeliveryLambdaPolicy \
    --policy-document file://backend/lambda-policy.json

# Deploy Lambda function
zip -j function.zip backend/lambda_function.py
aws lambda create-function \
    --function-name FoodDeliveryFunction \
    --runtime python3.12 \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::147997129747:role/FoodDeliveryLambdaRole \
    --zip-file fileb://function.zip
```

### 2. API Gateway Setup

```bash
# Create REST API
aws apigateway create-rest-api \
    --name FoodDeliveryAPI \
    --description "Food Delivery REST API"

# Create resource
aws apigateway create-resource \
    --rest-api-id ptwq1ckzk7 \
    --parent-id YOUR_ROOT_RESOURCE_ID \
    --path-part order

# Create methods
aws apigateway put-method \
    --rest-api-id ptwq1ckzk7 \
    --resource-id YOUR_RESOURCE_ID \
    --http-method POST \
    --authorization-type NONE

aws apigateway put-method \
    --rest-api-id ptwq1ckzk7 \
    --resource-id YOUR_RESOURCE_ID \
    --http-method GET \
    --authorization-type NONE

aws apigateway put-method \
    --rest-api-id ptwq1ckzk7 \
    --resource-id YOUR_RESOURCE_ID \
    --http-method OPTIONS \
    --authorization-type NONE

# Configure CORS
aws apigateway put-method-response \
    --rest-api-id ptwq1ckzk7 \
    --resource-id YOUR_RESOURCE_ID \
    --http-method OPTIONS \
    --status-code 200 \
    --response-parameters '{
        "method.response.header.Access-Control-Allow-Headers": true,
        "method.response.header.Access-Control-Allow-Methods": true,
        "method.response.header.Access-Control-Allow-Origin": true,
        "method.response.header.Access-Control-Max-Age": true
    }'

# Deploy API
aws apigateway create-deployment --rest-api-id ptwq1ckzk7
aws apigateway update-stage \
    --rest-api-id ptwq1ckzk7 \
    --stage-name prod \
    --deployment-id YOUR_DEPLOYMENT_ID
```

### 3. Frontend Deployment

```bash
# Create S3 bucket
aws s3 mb s3://food-delivery-frontend

# Enable static website hosting
aws s3 website --index-document index.html --error-document error.html s3://food-delivery-frontend

# Upload frontend files
aws s3 cp frontend/ s3://food-delivery-frontend/ --recursive
```

### 4. Monitoring Setup

```bash
# Create SNS topic for alerts
aws sns create-topic --name FoodDeliveryAlerts

# Subscribe email to SNS topic
aws sns subscribe \
    --topic-arn arn:aws:sns:ap-northeast-2:147997129747:FoodDeliveryAlerts \
    --protocol email \
    --notification-endpoint your-email@example.com

# Create CloudWatch alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "Lambda-FoodDelivery-Error-Alarm" \
    --metric-name "Errors" \
    --namespace "AWS/Lambda" \
    --statistic "Sum" \
    --period 300 \
    --threshold 1 \
    --comparison-operator "GreaterThanOrEqualToThreshold" \
    --dimensions Name=FunctionName,Value=FoodDeliveryFunction \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:ap-northeast-2:147997129747:FoodDeliveryAlerts \
    --ok-actions arn:aws:sns:ap-northeast-2:147997129747:FoodDeliveryAlerts \
    --alarm-description "Alarm if Lambda FoodDeliveryFunction has any errors."
```

## 🧪 Testing

### Create Order
```bash
curl -X POST https://ptwq1ckzk7.execute-api.ap-northeast-2.amazonaws.com/prod/order \
    -H "Content-Type: application/json" \
    -d '{"orderId": "123", "item": "Pizza"}'
```

### Get Order
```bash
curl https://ptwq1ckzk7.execute-api.ap-northeast-2.amazonaws.com/prod/order?orderId=123
```

## 🔒 IAM Role & Permissions

The Lambda function uses the following IAM role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:ap-northeast-2:147997129747:table/FoodOrders"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

## 🌟 Live Demo

Visit the live demo at: [Food Delivery System](https://food-delivery-irmuun.s3.ap-northeast-2.amazonaws.com/index.html)

## 📊 Monitoring & Observability

### CloudWatch Logs
- Log retention period: 14 days
- Structured logging implemented for all Lambda operations
- Logs include request/response details and error information

### CloudWatch Alarms
- **Error Monitoring**: Alerts on Lambda function errors
- **Throttle Monitoring**: Alerts on Lambda function throttling
- **Notification Channel**: SNS topic for alert delivery

### Performance Metrics
- Lambda execution time
- DynamoDB read/write capacity utilization
- API Gateway request counts and latency

### Business KPIs
- **Order Value Tracking**: Custom CloudWatch metrics for monitoring total order value
- **X-Ray Tracing**: Distributed tracing for request flow analysis
- **Cost Attribution**: Resource tagging for cost tracking and optimization

## 🧭 Project Scope & Possible Extensions

This project is designed as a cloud infrastructure and DevOps showcase, focusing on system architecture, AWS service integration, and the principles of the AWS Well-Architected Framework.

Common production-level features such as user authentication, API key enforcement, WAF integration, custom domain setup with Route53, CloudFront CDN, payment processing, and a full admin dashboard are intentionally omitted. These components, while important in real-world applications, are not required for demonstrating the core infrastructure and system design skills this project aims to highlight.

Such features could be added for a production deployment but are considered out of scope for this portfolio-focused project.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📢 Notes

- The project follows AWS best practices for serverless architecture
- All components are properly documented and commented
- The frontend is optimized for mobile and desktop viewing
- Error handling and validation are implemented throughout
- Comprehensive monitoring and alerting system in place 