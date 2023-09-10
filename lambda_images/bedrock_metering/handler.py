import json
import boto3
from aws_lambda_powertools import Logger

# Logger for CloudWatch logs
logger = Logger()


def count_tokens(text):
    return True


def lambda_handler(event, context):
    try:
        logger.info(event)
        return {"statusCode": 200, "body": "OK"}

    except Exception as e:
        logger.exception(e)
        return {"statusCode": 500, "body": str(e)}
