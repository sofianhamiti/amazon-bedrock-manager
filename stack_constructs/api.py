from constructs import Construct
from aws_cdk import aws_apigateway as apigw


class API(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        api_name: str,
        lambda_function_bedrock_api: str,
        lambda_function_api_authorizer: str,
    ):
        super().__init__(scope, id)

        # ==================================================
        # ============== LAMBDA AUTHORIZER =================
        # ==================================================
        # self.lambda_authorizer = apigw.TokenAuthorizer(
        #     scope=self,
        #     id="lambda-authorizer",
        #     handler=lambda_function_api_authorizer.current_version,
        # )

        # ==================================================
        # ===================== API ========================
        # ==================================================
        self.api = apigw.LambdaRestApi(
            scope=self,
            id="api_gateway",
            rest_api_name=api_name,
            handler=lambda_function_bedrock_api.current_version,
            proxy=True,
            # default_method_options=apigw.MethodOptions(
            #     authorizer=self.lambda_authorizer,
            #     authorization_type=apigw.AuthorizationType.CUSTOM
            # ),
        )

        # # Add mapping template
        # template = self.api.add_mapping_template(
        #     key="application/json", value={"generated_text": "$input.body"}
        # )
