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

        # ==========================
        # ======== CONFIG  =========
        # ==========================
        api_name = "bedrock-api"
        lambda_directory = "lambda_image"

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        lambda_function = LambdaFunction(
            self,
            "lambda_function",
            function_name=api_name,
            directory=lambda_directory,
        )
        # ==================================================
        # ================== API GATEWAY ===================
        # ==================================================
        api = API(
            scope=self,
            id="api",
            api_name=api_name,
            lambda_function=lambda_function.lambda_function,
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
