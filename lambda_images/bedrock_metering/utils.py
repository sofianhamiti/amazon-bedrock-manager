import time
import boto3
import datetime
import pandas as pd

MODEL_PRICES = {
    "amazon.titan-tg1-large": {"input_cost": 0, "output_cost": 0},
    "amazon.titan-e1t-medium": {"input_cost": 0, "output_cost": 0},
    "amazon.titan-embed-g1-text-02": {"input_cost": 0, "output_cost": 0},
    "stability.stable-diffusion-xl": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-grande-instruct": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-jumbo-instruct": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-mid": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-ultra": {"input_cost": 0, "output_cost": 0},
    "anthropic.claude-instant-v1": {"input_cost": 0, "output_cost": 0},
    "anthropic.claude-v1": {"input_cost": 0, "output_cost": 0},
    "anthropic.claude-v2": {"input_cost": 11.02, "output_cost": 32.68},
}


def get_model_pricing(model_id):
    model_info = MODEL_PRICES.get(model_id)
    if model_info:
        return model_info
    else:
        return None


def run_query(query, log_group_name):
    cloudwatch = boto3.client("logs")

    max_retries = 5

    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=1)
    end = now

    response = cloudwatch.start_query(
        logGroupName=log_group_name,
        startTime=int(start.timestamp() * 1000),
        endTime=int(end.timestamp() * 1000),
        queryString=query,
    )

    query_id = response["queryId"]

    retry_count = 0

    while True:
        response = cloudwatch.get_query_results(queryId=query_id)

        if response["results"] or retry_count == max_retries:
            break

        time.sleep(2)
        retry_count += 1

    return response["results"]


def results_to_df(results):
    column_names = set()
    rows = []

    for result in results:
        row = {
            item["field"]: item["value"]
            for item in result
            if "@ptr" not in item["field"]
        }
        column_names.update(row.keys())
        rows.append(row)

    df = pd.DataFrame(rows, columns=list(column_names))
    return df


def calculate_cost(row):
    try:
        input_token_count = float(row["input_token"])
        output_token_count = float(row["output_token"])
        model_id = row["model_id"]

        # get model pricing from utils
        model_pricing = get_model_pricing(model_id)

        # calculate costs of prompt and completion
        input_cost = input_token_count * model_pricing["input_cost"] / 1000
        output_cost = output_token_count * model_pricing["output_cost"] / 1000

        return input_cost, output_cost
    except (ValueError, KeyError):
        # Handle cases where data is not in the expected format
        return None, None
