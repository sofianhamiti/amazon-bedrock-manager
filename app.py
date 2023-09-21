from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Stack,
    App,
)

from stack_constructs.api import API
from stack_constructs.lambda_function import LambdaFunction


class APIStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ==================================================
        # ================= PARAMETERS =====================
        # ==================================================
        api_name = "bedrock-api"
        directory_bedrock_api = "lambda_images/bedrock_api"

        metering_name = "bedrock-metering"
        directory_usage_aggregator = "lambda_images/bedrock_metering"

        # ==================================================
        # ================== BEDROCK API ===================
        # ==================================================
        lambda_function_bedrock_api = LambdaFunction(
            scope=self,
            id="lambda_function_bedrock_api",
            function_name=api_name,
            directory=directory_bedrock_api,
            provisioned_concurrency=False,
            metering_function_name=metering_name,
        )

        api = API(
            scope=self,
            id="api",
            api_name=api_name,
            lambda_function=lambda_function_bedrock_api.lambda_function,
        )

        # ==================================================
        # ==================== METERING ====================
        # ==================================================
        lambda_function_bedrock_metering = LambdaFunction(
            scope=self,
            id="lambda_function_metering",
            function_name=metering_name,
            directory=directory_usage_aggregator,
            provisioned_concurrency=False,
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
