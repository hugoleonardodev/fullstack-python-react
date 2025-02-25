import json
import os
import boto3
import logging
from datetime import datetime
import pymongo

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = os.environ.get('DB_NAME', 'ecommerce')

# Initialize AWS services
sns = boto3.client('sns')
s3 = boto3.client('s3')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
S3_BUCKET = os.environ.get('S3_BUCKET')

def get_mongo_client():
    """Create and return a MongoDB client."""
    return pymongo.MongoClient(MONGO_URI)

def process_new_order(order_data):
    """
    Process a new order and send notification.
    """
    logger.info(f"Processing new order: {order_data.get('_id')}")
    
    # Send SNS notification
    message = {
        'message': f"New order created: {order_data.get('_id')}",
        'order_id': str(order_data.get('_id')),
        'customer': order_data.get('customer_id'),
        'total_amount': order_data.get('total_amount'),
        'created_at': order_data.get('created_at').isoformat() if isinstance(order_data.get('created_at'), datetime) else order_data.get('created_at')
    }
    
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=json.dumps(message),
        Subject='New Order Notification'
    )
    
    logger.info(f"Notification sent for order: {order_data.get('_id')}")

def generate_sales_report():
    """
    Generate a sales report based on orders and upload to S3.
    """
    logger.info("Generating sales report")
    
    client = get_mongo_client()
    db = client[DB_NAME]
    orders_collection = db.orders
    
    # Get orders from the last 24 hours
    yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    pipeline = [
        {
            "$match": {
                "created_at": {"$gte": yesterday}
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "total": {"$sum": "$total_amount"}
            }
        }
    ]
    
    result = list(orders_collection.aggregate(pipeline))
    
    # Generate report content
    report = {
        "generated_at": datetime.now().isoformat(),
        "period": f"From {yesterday.isoformat()}",
        "summary": result,
    }
    
    # Upload report to S3
    report_key = f"reports/sales/daily/{datetime.now().strftime('%Y-%m-%d')}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=report_key,
        Body=json.dumps(report),
        ContentType='application/json'
    )
    
    logger.info(f"Sales report uploaded to S3: {report_key}")
    client.close()
    
    return {
        "report_location": f"s3://{S3_BUCKET}/{report_key}",
        "summary": report
    }

def lambda_handler(event, context):
    """
    Main Lambda handler function.
    
    This function handles different event types:
    1. New order events (triggered by MongoDB change stream)
    2. Scheduled events for generating sales reports
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Check event type
        if event.get('detail-type') == 'Scheduled Event':
            # This is a scheduled event (e.g., daily report generation)
            result = generate_sales_report()
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
            
        elif event.get('source') == 'aws.events' and event.get('detail', {}).get('eventType') == 'INSERT':
            # This is a new order event from MongoDB change stream
            order_data = event.get('detail', {}).get('fullDocument', {})
            process_new_order(order_data)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f"Order {order_data.get('_id')} processed successfully"
                })
            }
            
        elif event.get('httpMethod'):
            # This is an HTTP API Gateway event
            body = json.loads(event.get('body', '{}'))
            action = body.get('action')
            
            if action == 'generate_report':
                result = generate_sales_report()
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps(result)
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Invalid action specified'
                    })
                }
                
        else:
            logger.warning(f"Unhandled event type: {event}")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Unhandled event type'
                })
            }
            
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
