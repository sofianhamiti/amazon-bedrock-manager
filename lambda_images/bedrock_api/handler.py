import json
import boto3
import asyncio
from botocore.config import Config
from aws_lambda_powertools import Logger

# Bedrock client
bedrock = boto3.client(
    service_name="bedrock",
    region_name="us-east-1",
    endpoint_url="https://bedrock.us-east-1.amazonaws.com",
    config=Config(retries={"max_attempts": 3, "mode": "adaptive"}),
)

# Logger for CloudWatch logs
logger = Logger()


def prepare_payload(event_body):
    return json.dumps({"prompt": event_body["inputs"], **event_body["parameters"]})


def invoke_bedrock(payload, model_id, user_id):
    response = bedrock.invoke_model(
        body=payload,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        # Get text reponse from the model
        completion = json.loads(response.get("body").read())["completion"]
        return completion

    else:
        raise Exception(
            "Bedrock API call failed with status "
            + str(response["ResponseMetadata"]["HTTPStatusCode"])
        )


def log_api_call(user_id, prompt, completion, model_id):
    logger.append_keys(user_id=user_id)
    logger.append_keys(model_id=model_id)
    logger.append_keys(prompt=prompt)
    logger.append_keys(completion=completion)
    logger.info("api call")


def lambda_handler(event, context):
    try:
        bedrock_payload = prepare_payload(json.loads(event["body"]))

        user_id = event["headers"]["user_id"]
        model_id = event["headers"]["model_id"]
        completion = invoke_bedrock(
            payload=bedrock_payload,
            model_id=model_id,
            user_id=user_id,
        )

        log_api_call(
            user_id=user_id,
            prompt=bedrock_payload,
            completion=completion,
            model_id=model_id,
        )

        return {"statusCode": 200, "body": json.dumps([{"generated_text": completion}])}

    except Exception as e:
        logger.exception(e)
        return {"statusCode": 500, "body": json.dumps([{"error": str(e)}])}
