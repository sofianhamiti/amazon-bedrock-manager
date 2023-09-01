import json
import boto3
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


def invoke_bedrock(event_body, model_id):
    payload = prepare_payload(event_body)
    response = bedrock.invoke_model(
        body=payload,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        # Get text reponse from the model
        completion = json.loads(response.get("body").read())["completion"]

        log_api_call(
            user="user1",
            prompt=event_body["inputs"],
            completion=completion,
            model_id=model_id,
        )
        return completion
    else:
        raise Exception(
            "Bedrock API call failed with status "
            + str(response["ResponseMetadata"]["HTTPStatusCode"])
        )


def prepare_payload(event_body):
    return json.dumps({"prompt": event_body["inputs"], **event_body["parameters"]})


def log_api_call(user, prompt, completion, model_id):
    logger.append_keys(user=user)
    logger.append_keys(model_id=model_id)
    logger.append_keys(prompt=prompt)
    logger.append_keys(completion=completion)
    logger.info("api call")


def lambda_handler(event, context):
    try:
        completion = invoke_bedrock(
            event_body=json.loads(event["body"]), model_id=event["headers"]["model_id"]
        )
        return {"statusCode": 200, "body": json.dumps([{"generated_text": completion}])}

    except Exception as e:
        logger.exception(e)
        return {"statusCode": 500, "body": json.dumps([{"error": str(e)}])}
