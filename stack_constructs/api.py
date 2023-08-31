from constructs import Construct
from aws_cdk import aws_apigateway as apigw


class API(Construct):
    def __init__(self, scope: Construct, id: str, api_name: str, lambda_function: str):
        super().__init__(scope, id)

        self.api = apigw.LambdaRestApi(
            scope=self,
            id="api_gateway",
            rest_api_name=api_name,
            handler=lambda_function,
            proxy=True,
        )


