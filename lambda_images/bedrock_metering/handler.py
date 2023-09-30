import os
from utils import run_query, results_to_df, calculate_cost

QUERY_BEDROCK = """
fields requestId as request_id_bedrock, modelId as model_id, input.inputTokenCount as input_token, output.outputTokenCount as output_token 
| filter operation = "InvokeModel"
"""

QUERY_API = """
fields message.request_id as request_id_lambda, message.cost_center as cost_center
| filter level = "INFO"
"""

log_group_name_bedrock = os.environ["LOG_GROUP_BEDROCK"]
log_group_name_api = os.environ["LOG_GROUP_API"]


def process_event(event):
    # querying the cloudwatch logs from Bedrock
    query_results_bedrock = run_query(QUERY_BEDROCK, log_group_name_bedrock)
    df_bedrock = results_to_df(query_results_bedrock)

    # querying the cloudwatch logs from the API
    query_results_api = run_query(QUERY_API, log_group_name_api)
    df_api = results_to_df(query_results_api)

    # merging the results using the request_id field
    df_bedrock_metering = df_bedrock.merge(
        df_api, left_on="request_id_bedrock", right_on="request_id_lambda"
    )

    # Apply the calculate_cost function to the DataFrame
    df_bedrock_metering[["input_cost", "output_cost"]] = df_bedrock_metering.apply(
        calculate_cost, axis=1, result_type="expand"
    )

    # aggregate cost for each cost center
    df_bedrock_metering_aggregated = df_bedrock_metering.groupby("cost_center").sum()[
        ["input_cost", "output_cost"]
    ]

    print(df_bedrock_metering_aggregated)


def lambda_handler(event, context):
    try:
        process_event(event)
        return {"statusCode": 200, "body": "OK"}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": str(e)}
