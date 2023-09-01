from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    Duration,
)


class LambdaFunction(Construct):
    def __init__(self, scope: Construct, id: str, function_name: str, directory: str):
        super().__init__(scope, id)

        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        self.lambda_role = iam.Role(
            scope=self,
            id="lambda_role",
            role_name=function_name,
            assumed_by=iam.ServicePrincipal(service="lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ],
        )

        # ==================================================
        # =================== ECR IMAGE ====================
        # ==================================================
        self.ecr_image = lambda_.DockerImageCode.from_image_asset(directory=directory)

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        self.lambda_function = lambda_.DockerImageFunction(
            scope=self,
            id="lambda",
            function_name=function_name,
            code=self.ecr_image,
            memory_size=512,
            role=self.lambda_role,
            timeout=Duration.seconds(60),
        )
        # ==================================================
        # ============ PROVISIONED CONCURRENCY =============
        # ==================================================
        self.alias = lambda_.Alias(
            scope=self,
            id="lambda_alias",
            alias_name="Prod",
            version=self.lambda_function.current_version,
            provisioned_concurrent_executions=100,
        )