import os
import json
import boto3
from botocore.config import Config

# Lambda client
lambda_client = boto3.client("lambda")
metering_function_name = os.environ["METERING_FUNCTION"]
cost_center = os.environ["COST_CENTER"]

# Bedrock client
bedrock = boto3.client(
    service_name="bedrock",
    region_name="us-east-1",
    endpoint_url="https://bedrock.us-east-1.amazonaws.com",
    config=Config(retries={"max_attempts": 3, "mode": "adaptive"}),
)


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
        # Get text reponse from the model
        completion = json.loads(response.get("body").read())["completion"]
        return completion

    else:
        raise Exception(
            "Bedrock API call failed with status "
            + str(response["ResponseMetadata"]["HTTPStatusCode"])
        )


def log_api_call(payload):
    # log the api call with the metering lambda function
    lambda_client.invoke(
        FunctionName=metering_function_name,
        InvocationType="Event",  # Use asynchronous invocation
        Payload=json.dumps(payload),
    )


def lambda_handler(event, context):
    try:
        print(event)
        bedrock_payload = prepare_bedrock_payload(json.loads(event["body"]))
        model_id = event["headers"]["model_id"]

        completion = invoke_bedrock(
            payload=bedrock_payload,
            model_id=model_id,
        )

        log_api_call(
            {
                "cost_center": cost_center,
                "model_id": model_id,
                "prompt": bedrock_payload,
                "completion": completion,
            }
        )
        return {"statusCode": 200, "body": json.dumps([{"generated_text": completion}])}
        # return {"statusCode": 200, "body": completion}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps([{"generated_text": str(e)}])}
        # return {"statusCode": 500, "body": str(e)}
