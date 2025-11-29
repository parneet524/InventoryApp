import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if o % 1 == 0:
                return int(o)
            return float(o)
        return super().default(o)

def lambda_handler(event, context):
    params = event.get("pathParameters", {})
    item_id = params.get("id")

    location_id = event.get("queryStringParameters", {}).get("location_id")
    if location_id is None:
        return {"statusCode": 400, "body": "Missing location_id"}

    try:
        location_id = int(location_id)
        result = table.get_item(Key={"item_id": item_id, "location_id": location_id})
        if "Item" not in result:
            return {"statusCode": 404, "body": "Item not found"}

        return {
            "statusCode": 200,
            "body": json.dumps(result["Item"], cls=DecimalEncoder)
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}

