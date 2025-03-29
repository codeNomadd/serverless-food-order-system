# 🍽️ Food Delivery REST API

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

1. **Frontend Layer**
   - Static website hosted on S3
   - Responsive design with Tailwind CSS
   - Client-side validation and error handling

2. **API Layer**
   - RESTful endpoints (/order)
   - CORS support for cross-origin requests
   - Request/response validation

3. **Backend Layer**
   - Serverless Lambda function
   - DynamoDB for data persistence
   - CloudWatch for logging and monitoring
   - SNS for error notifications

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
      "Resource": "*"
    }
  ]
}
```

## 🌐 Live Demo

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

## ✅ Future Improvements

- [ ] User Authentication
  - Signup/Login functionality
  - JWT token-based auth
  - User profile management

- [ ] Admin Dashboard
  - Order management
  - Analytics and reporting
  - User management

- [ ] Enhanced Security
  - HTTPS via Route53 and CloudFront
  - API key authentication
  - Rate limiting

- [ ] Development Experience
  - Docker for local testing
  - CI/CD pipeline
  - Automated testing

- [ ] Payment Integration
  - Stripe/PayPal integration
  - Order status tracking
  - Payment history

## 🚀 Further Enhancements

### Implemented ✅
- **API Gateway Throttling Configured**: Rate limiting is set up to protect against excessive requests and prevent billing spikes.
- **DynamoDB Auto Scaling & Backups**: Enabled auto-scaling (5-20 units) for both read and write capacity, with Point-in-Time Recovery (PITR) configured for continuous 35-day backup protection.

### Planned Improvements
- **CloudWatch Monitoring & Alarms**: Enable detailed monitoring of Lambda execution time, error rates, and throttling. Set CloudWatch Alarms to notify when errors or high usage occur.
- **AWS WAF Integration**: Attach AWS Web Application Firewall (WAF) to the API Gateway to protect against bots, SQL injections, XSS attacks, and spammers.
- **CloudFront CDN**: Add CloudFront caching for the frontend and API responses to reduce latency and Lambda invocations under high load.
- **AWS Budgets & Cost Monitoring**: Set budget alerts to avoid unexpected costs if the API gets discovered and heavily used.
- **API Key & Usage Plans**: Strengthen API access control by requiring API keys and setting usage plans with quotas and rate limits.
- **Domain Name & HTTPS**: Use Route53 and AWS Certificate Manager (ACM) to add a custom domain with HTTPS for a production-grade professional deployment.

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 📢 Notes

- The project follows AWS best practices for serverless architecture
- All components are properly documented and commented
- The frontend is optimized for mobile and desktop viewing
- Error handling and validation are implemented throughout
- Comprehensive monitoring and alerting system in place 