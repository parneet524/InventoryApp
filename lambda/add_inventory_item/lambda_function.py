import json
import boto3
import ulid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

def lambda_handler(event, context):
    body = json.loads(event["body"])

    item = {
        "item_id": str(ulid.new()),
        "location_id": int(body["location_id"]),
        "name": body["name"],
        "description": body["description"],
        "qty_on_hand": int(body["qty_on_hand"]),
        "price": float(body["price"])
    }

    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Item created", "item": item})
    }

