import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    item_id = event["pathParameters"]["id"]
    location_id = int(event["queryStringParameters"]["location_id"])

    result = table.get_item(Key={"item_id": item_id, "location_id": location_id})
    if "Item" not in result:
        return {"statusCode": 404, "body": "Item not found"}

    table.delete_item(Key={"item_id": item_id, "location_id": location_id})

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Item deleted", "id": item_id})
    }

