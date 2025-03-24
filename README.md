# 🍽️ Food Delivery REST API

A serverless food delivery system built with AWS Lambda, API Gateway, and DynamoDB.

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
└── infra/                    # Infrastructure policies
    └── trust-policy.json     # IAM trust policy for Lambda
```

## 🏗️ Architecture

### Backend Flow
1. API Gateway receives HTTP requests
2. Lambda function processes requests:
   - POST /order: Creates new order in DynamoDB
   - GET /order: Retrieves order details
   - OPTIONS: Handles CORS preflight
3. DynamoDB stores and retrieves order data

### Frontend Flow
1. Static files hosted on S3
2. HTML/JS makes API calls to API Gateway
3. User interface updates based on API responses
4. CORS enabled for secure cross-origin requests

### IAM Role & Permissions
- `FoodDeliveryLambdaRole`: Allows Lambda to:
  - Access DynamoDB (PutItem, GetItem)
  - Write CloudWatch Logs
  - Execute with proper security context

### S3 Static Hosting
- Frontend files served from S3 bucket
- Configured for static website hosting
- CORS enabled for API communication

## 🚀 Setup & Deployment

### 1. Backend Setup
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

## 🔒 IAM Execution Role & Permissions

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

## 📝 License

MIT License 