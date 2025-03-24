import json
import boto3

# Set up DynamoDB connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FoodOrders')

def lambda_handler(event, context):
    # Get the HTTP method from the request
    http_method = event['httpMethod']

    # Handle CORS preflight requests
    if http_method == 'OPTIONS':
        return build_cors_response()

    # Create new order
    if http_method == 'POST':
        body = json.loads(event['body'])
        order_id = body['orderId']
        item = body['item']
        table.put_item(Item={'orderId': order_id, 'item': item})
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
