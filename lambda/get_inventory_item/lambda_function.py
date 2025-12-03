import json
import boto3
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

    item_id = event["pathParameters"]["item_id"]
    location_id = int(event["pathParameters"]["location_id"])

    response = table.get_item(
        Key={
            "item_id": item_id,
            "location_id": location_id
        }
    )

    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }

    item = convert_decimal(response["Item"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item)
    }

