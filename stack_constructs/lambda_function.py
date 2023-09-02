from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    Duration,
)


class LambdaFunction(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        function_name: str,
        directory: str,
        provisioned_concurrency: bool,
    ):
        super().__init__(scope, id)

        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        self.lambda_role = iam.Role(
            self,
            "LambdaRole",
            assumed_by=iam.ServicePrincipal(service="lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambdaExecute")
            ],
        )

        self.sagemaker_policy = iam.Policy(
            scope=self,
            id="bedrock_access",
            policy_name="bedrock-access",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "bedrock:*",
                    ],
                    resources=["*"],
                )
            ],
        )
        self.sagemaker_policy.attach_to_role(self.lambda_role)

        # ==================================================
        # =================== ECR IMAGE ====================
        # ==================================================
        self.ecr_image = lambda_.DockerImageCode.from_image_asset(directory=directory)

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        self.lambda_function = lambda_.DockerImageFunction(
            scope=self,
            id="lambda_function",
            function_name=function_name,
            code=self.ecr_image,
            memory_size=512,
            role=self.lambda_role,
            timeout=Duration.seconds(60),
        )
        # ==================================================
        # ============ PROVISIONED CONCURRENCY =============
        # ==================================================
        if provisioned_concurrency:
            self.alias = lambda_.Alias(
                scope=self,
                id="lambda_alias",
                alias_name="Prod",
                version=self.lambda_function.current_version,
                provisioned_concurrent_executions=100,
            )
