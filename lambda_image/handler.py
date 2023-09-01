import json
import boto3
from botocore.config import Config
from aws_lambda_powertools import Logger

# CREATE BEDROCK CLIENT
bedrock = boto3.client(
    service_name="bedrock",
    region_name="us-east-1",
    endpoint_url="https://bedrock.us-east-1.amazonaws.com",
    config=Config(retries={"max_attempts": 3, "mode": "adaptive"}),
)

# CREATE LOGGER FROM LAMBDA POWER TOOLS
logger = Logger()


def lambda_handler(event, context):
    event_body = json.loads(event["body"])

    try:
        # PREPARING PAYLOAD
        model_id = event["headers"]["model_id"]
        payload_body = json.dumps(
            {**{"prompt": event_body["inputs"]}, **event_body["parameters"]}
        )

        # INVOKE BEDROCK
        bedrock_response = bedrock.invoke_model(
            body=payload_body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        # IF SUCCESS, SEND RESPONSE TO USER
        if bedrock_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            # LOG THE INPUT TOKEN SIZE
            input_token_size = 256
            logger.append_keys(user="user1")
            logger.append_keys(model_id=model_id)
            logger.append_keys(token_size=input_token_size)
            logger.info("input")

            response_body = json.loads(bedrock_response.get("body").read())[
                "completion"
            ]

            # LOG THE OUTPUT TOKEN SIZE
            output_token_size = 512
            logger.append_keys(user="user1")
            logger.append_keys(model_id=model_id)
            logger.append_keys(token_size=output_token_size)
            logger.info("output")

            return {
                "statusCode": 200,
                "body": json.dumps([{"generated_text": response_body}]),
            }
        else:
            # Status code was not 200, raise exception
            raise Exception(
                "Bedrock API call failed with status "
                + str(bedrock_response["ResponseMetadata"]["HTTPStatusCode"])
            )

    except Exception as e:
        logger.exception(e)
        return {
            "statusCode": 500,
            "body": json.dumps([{"generated_text": e}]),
        }
