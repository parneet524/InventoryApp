import json
import boto3
from boto3.dynamodb.conditions import Key
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
    location_id = int(event["pathParameters"]["id"])

    result = table.query(
        IndexName="location_index",
        KeyConditionExpression=Key("location_id").eq(location_id)
    )

    return {
        "statusCode": 200,
        "body": json.dumps(result["Items"], cls=DecimalEncoder)
    }

