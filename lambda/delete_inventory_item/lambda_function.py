import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Inventory')

def lambda_handler(event, context):
    item_id = event["pathParameters"]["item_id"]
    location_id = int(event["pathParameters"]["location_id"])

    # Check if it exists first
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

    # Delete the item
    table.delete_item(
        Key={
            "item_id": item_id,
            "location_id": location_id
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Item deleted"})
    }
