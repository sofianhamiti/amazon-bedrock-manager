import json

# from langchain.memory import DynamoDBChatMessageHistory


def lambda_handler(event, context):
    try:
        model_id = event["headers"]["model_id"]
        # event_body = json.loads(event["body"])
        # print(event_body)
        return {"statusCode": 200, "body": json.dumps([{"generated_text": "ZEUUBBBB"}])}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": str(e)}
