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

        authorizer_name = "bedrock-authorizer"
        directory_api_authorizer = "lambda_images/api_authorizer"

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

        lambda_function_api_authorizer = LambdaFunction(
            scope=self,
            id="lambda_function_api_authorizer",
            function_name=authorizer_name,
            directory=directory_api_authorizer,
            provisioned_concurrency=False,
        )

        api = API(
            scope=self,
            id="api",
            api_name=api_name,
            lambda_function_bedrock_api=lambda_function_bedrock_api.lambda_function,
            lambda_function_api_authorizer=lambda_function_api_authorizer.lambda_function,
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
