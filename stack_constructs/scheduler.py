from constructs import Construct
from aws_cdk import (
    aws_events as events,
    aws_events_targets as targets,
)


class LambdaFunctionScheduler(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        lambda_function: str,
        cron_scheduling_expression: str,
    ):
        super().__init__(scope, id)

        # ==================================================
        # ================== SCHEDULING ====================
        # ==================================================
        self.cron_rule = events.Rule(
            scope=self,
            id="cron_rule",
            rule_name="usage_aggregator_schedule",
            schedule=events.Schedule.expression(cron_scheduling_expression),
        )

        self.cron_rule.add_target(target=targets.LambdaFunction(lambda_function))
