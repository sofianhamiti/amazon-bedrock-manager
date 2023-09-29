from constructs import Construct
from aws_cdk import CfnOutput, Stack, App, Tags

from stack_constructs.api import API
from stack_constructs.lambda_function import LambdaFunction
from stack_constructs.scheduler import LambdaFunctionScheduler


class BedrockAPIStack(Stack):
    def __init__(self, scope: Construct, id: str, cost_center: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ==================================================
        # ================= PARAMETERS =====================
        # ==================================================
        api_name = f"{cost_center}-bedrock-api"
        directory_bedrock_api = "lambda_images/bedrock_api"

        metering_name = f"{cost_center}-bedrock-metering"
        directory_bedrock_metering = "lambda_images/bedrock_metering"

        # ==================================================
        # ================== BEDROCK API ===================
        # ==================================================
        lambda_function_bedrock_api = LambdaFunction(
            scope=self,
            id="lambda_function_bedrock_api",
            function_name=api_name,
            directory=directory_bedrock_api,
            environment={
                "COST_CENTER": cost_center,
            },
        )

        api = API(
            scope=self,
            id="bedrock-api",
            api_name=api_name,
            lambda_function_bedrock_api=lambda_function_bedrock_api.lambda_function,
        )

        # ==================================================
        # =================== METERING =====================
        # ==================================================
        lambda_function_bedrock_metering = LambdaFunction(
            scope=self,
            id="lambda_function_bedrock_metering",
            function_name=metering_name,
            directory=directory_bedrock_metering,
        )

        scheduler_usage_aggregator = LambdaFunctionScheduler(
            scope=self,
            id="usage_aggregator_scheduler",
            lambda_function=lambda_function_bedrock_metering.lambda_function,
        )

        # ==================================================
        # =================== OUTPUTS ======================
        # ==================================================
        CfnOutput(
            scope=self,
            id="APIURL",
            value=api.api.url,
        )


# ==================================================
# ============== STACK WITH COST CENTER ============
# ==================================================
cost_center = "abc"

app = App()
api_stack = BedrockAPIStack(
    scope=app, id=f"{cost_center}-Bedrock-API", cost_center=cost_center
)
# Add a cost tag to all constructs in the stack
Tags.of(api_stack).add("CostCenter", cost_center)

app.synth()
