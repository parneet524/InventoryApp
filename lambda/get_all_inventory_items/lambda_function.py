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
    try:
        response = table.scan()
        items = response.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps(items, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

