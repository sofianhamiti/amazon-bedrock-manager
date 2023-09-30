import os
import json
import boto3
from botocore.config import Config
from aws_lambda_powertools import Logger

cost_center = os.environ["COST_CENTER"]

# Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    config=Config(retries={"max_attempts": 3, "mode": "adaptive"}),
)

# Logger for CloudWatch logs
logger = Logger()


def prepare_bedrock_payload(event_body):
    return json.dumps({"prompt": event_body["inputs"], **event_body["parameters"]})


def invoke_bedrock(payload, model_id):
    response = bedrock.invoke_model(
        body=payload,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        # Get text reponse from the model and request ID to map request to cost centre
        completion = json.loads(response.get("body").read())["completion"]
        request_id = response["ResponseMetadata"]["RequestId"]
        return completion, request_id

    else:
        raise Exception(
            "Bedrock API call failed with status "
            + str(response["ResponseMetadata"]["HTTPStatusCode"])
        )


def lambda_handler(event, context):
    try:
        # print(event)
        bedrock_payload = prepare_bedrock_payload(json.loads(event["body"]))
        model_id = event["headers"]["model_id"]

        completion, request_id = invoke_bedrock(
            payload=bedrock_payload,
            model_id=model_id,
        )

        logger.info({"cost_center": cost_center, "requestId": request_id})

        return {"statusCode": 200, "body": json.dumps([{"generated_text": completion}])}
        # return {"statusCode": 200, "body": completion}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps([{"generated_text": str(e)}])}
        # return {"statusCode": 500, "body": str(e)}
