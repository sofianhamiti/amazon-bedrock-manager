from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Stack,
    App,
)

from stack_constructs.api import API
from stack_constructs.lambda_function import LambdaFunction
from stack_constructs.scheduler import LambdaFunctionScheduler


class APIStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ==================================================
        # ================= PARAMETERS =====================
        # ==================================================
        api_name = "bedrock-api"
        directory_bedrock_api = "lambda_images/bedrock_api"

        aggregator_name = "usage-aggregator"
        directory_usage_aggregator = "lambda_images/usage_aggregator"

        # ==================================================
        # ================== BEDROCK API ===================
        # ==================================================
        lambda_function_bedrock_api = LambdaFunction(
            scope=self,
            id="lambda_function_bedrock_api",
            function_name=api_name,
            directory=directory_bedrock_api,
            provisioned_concurrency=False,
        )

        api = API(
            scope=self,
            id="api",
            api_name=api_name,
            lambda_function=lambda_function_bedrock_api.lambda_function,
        )

        # ==================================================
        # ================ USAGE AGGREGATOR ================
        # ==================================================
        lambda_function_usage_aggregator = LambdaFunction(
            scope=self,
            id="lambda_function_usage_aggregator",
            function_name=aggregator_name,
            directory=directory_usage_aggregator,
            provisioned_concurrency=False,
        )

        usage_aggregator_scheduler = LambdaFunctionScheduler(
            scope=self,
            id="usage_aggregator_scheduler",
            lambda_function=lambda_function_usage_aggregator.lambda_function,
        )

        # ==================================================
        # =================== OUTPUTS ======================
        # ==================================================
        CfnOutput(
            scope=self,
            id="APIURL",
            value=api.api.url,
        )


app = App()
APIStack(app, "APIStack")
app.synth()
