import tiktoken
from utils import get_model_pricing
from aws_lambda_powertools import Logger

# Logger for CloudWatch logs
logger = Logger()


def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def calculate_request_cost(model_id, input_token_count, output_token_count):
    # get model pricing from utils
    model_pricing = get_model_pricing(model_id)

    # calculate costs of prompt and completion
    input_cost = input_token_count * model_pricing["input_cost"] / 1_000_000
    output_cost = output_token_count * model_pricing["output_cost"] / 1_000_000

    return {"prompt_cost": input_cost, "completion_cost": output_cost}


def process_request(event):
    event["prompt_tokens"] = count_tokens(event["prompt"])
    event["completion_tokens"] = count_tokens(event["completion"])

    request_cost = calculate_request_cost(
        model_id=event["model_id"],
        input_token_count=event["prompt_tokens"],
        output_token_count=event["completion_tokens"],
    )
    event.update(request_cost)
    logger.info(event)


def lambda_handler(event, context):
    try:
        # process_request(event)
        print("hello")
        return {"statusCode": 200, "body": "OK"}
    except Exception as e:
        logger.exception(e)
        return {"statusCode": 500, "body": str(e)}
