import builtins
from typing import List

import aws_cdk
from aws_cdk import aws_iam

from datalake_stack.datalake_stack import IotDataLakeStack
from scratch_stack.scratch_stack import IotScratchStack
from config.bucket_attributes import BucketAttributes
from analytics_stack.analytics_stack import AnalyticsStack


class RegionalStack(aws_cdk.Stack):
    def __init__(
        self,
        scope,
        application_ci: str,
        source_bucket: BucketAttributes,
        target_buckets: List[BucketAttributes],
        source_scratch_bucket: BucketAttributes,
        target_scratch_buckets: List[BucketAttributes],
        deploy_replication: bool,
        app_environment: str,
        credential_role_level: str,
        tag: str,
        aws_environment: aws_cdk.Environment,
        id: builtins.str,
        **kwargs,
    ):
        # application_ci=application_ci
        super().__init__(scope, id)
        prefix = ""
        if app_environment != "dev":
            prefix = "ADFS-"
        dev_role = aws_iam.Role.from_role_name(
            self,
            "ebrDevRole",
            role_name=f"""{prefix}-{app_environment.upper()}-OperationsTechnology_EBR-{credential_role_level.upper()}""",
        )

        datalake_stack = IotDataLakeStack(
            self,
            "datalake",
            application_ci=application_ci,
            bucket_name=source_bucket["bucket_name"],
            deploy_replication=deploy_replication,
            target_buckets=target_buckets,
            env=aws_environment,
        )

        scratch_stack = IotScratchStack(
            self,
            "scratch",
            application_ci=application_ci,
            bucket_name=source_scratch_bucket["bucket_name"],
            deploy_replication=deploy_replication,
            target_buckets=target_scratch_buckets,
            env=aws_environment,
        )

        analytics_stack = AnalyticsStack(
            self,
            "analytics",
            application_ci=application_ci,
            tag=tag,
            datalake_bucket_name=source_bucket["bucket_name"],
            demo_dataset_name="bike_sales",
            env=aws_environment,
        )
