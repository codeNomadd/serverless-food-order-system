import json
import boto3
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from botocore.config import Config
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configure boto3 with retries
config = Config(
    retries = dict(
        max_attempts = 3,
        mode = 'standard'
    )
)

# Initialize AWS clients with X-Ray
patch_all()
dynamodb = boto3.resource('dynamodb', config=config)
cloudwatch = boto3.client('cloudwatch')
table = dynamodb.Table('FoodOrders')

# Global variables for connection reuse
dynamodb = None
table = None

def get_dynamodb():
    global dynamodb, table
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('FoodOrders')
    return table

def record_order_metric(order_value):
    """Record custom metric for order value"""
    try:
        cloudwatch.put_metric_data(
            Namespace='FoodDelivery',
            MetricData=[
                {
                    'MetricName': 'OrderValue',
                    'Value': order_value,
                    'Unit': 'USD',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
    except Exception as e:
        logger.error(f"Failed to record order metric: {str(e)}")

@xray_recorder.capture('lambda_handler')
def lambda_handler(event, context):
    # Get the HTTP method from the request
    http_method = event['httpMethod']
    logger.info('Received event: %s', json.dumps(event))
    
    try:
        # Handle CORS preflight requests
        if http_method == 'OPTIONS':
            return build_cors_response()

        # Create new order
        if http_method == 'POST':
            body = json.loads(event['body'])
            order_id = body['orderId']
            item = body['item']
            price = body.get('price', 0)  # Default to 0 if not provided
            
            table.put_item(Item={
                'orderId': order_id,
                'item': item,
                'price': price,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Record order value metric
            record_order_metric(price)
            
            logger.info(f"Successfully processed order: {order_id}")
            return build_response(200, f"Order {order_id} for {item} received.")

        # Get order details
        elif http_method == 'GET':
            order_id = event['queryStringParameters']['orderId']
            response_data = table.get_item(Key={'orderId': order_id})
            if 'Item' in response_data:
                return build_response(200, response_data['Item'])
            else:
                return build_response(404, 'Order not found')

        return build_response(400, 'Unsupported HTTP method')
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return build_response(500, 'Internal server error')

def build_cors_response():
    """Build response for CORS preflight requests"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('CORS preflight successful')
    }

def build_response(status_code, body):
    """Build standard API response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(body)
    }
