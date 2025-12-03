import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_decimal(v) for v in obj]
    return obj

def lambda_handler(event, context):

    # Get location_id from path parameters
    location_id = int(event["pathParameters"]["location_id"])

    # Query using your GSI "location_index"
    response = table.query(
        IndexName="location_index",
        KeyConditionExpression=Key("location_id").eq(location_id)
    )

    items = convert_decimal(response.get("Items", []))

    return {
        "statusCode": 200,
        "body": json.dumps(items),
        "headers": {"Content-Type": "application/json"}
    }
