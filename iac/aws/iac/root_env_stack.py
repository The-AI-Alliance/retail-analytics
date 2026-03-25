import aws_cdk
import builtins
from aws_cdk import aws_events
from regional_stack import RegionalStack
from config.bucket_attributes import BucketAttributes
import os

# TODO: Wire in qa and prd when we get there...
account_ids = {
    "dev": os.environ["AWS_DEV_ACCOUNT_ID"],
    "qa": os.environ["AWS_QA_ACCOUNT_ID"],
    "prd": os.environ["AWS_PRD_ACCOUNT_ID"],
}


class RootEnvStack(aws_cdk.Stack):
    def __init__(
        self,
        scope,
        deploy_replication: bool,
        app_environment: str,
        environment: str,
        tag: str,
        id: builtins.str,
        *,
        application_ci: builtins.str,
        **kwargs,
    ):

        # application_ci=application_ci
        super().__init__(scope, id)

        bucket_base_name = f"""{application_ci}-datalake-{app_environment}"""
        secondary_bucket = BucketAttributes(
            bucket_name=f"{bucket_base_name}-{tag}us-east-1",
            region="us-east-1",
            account=self.account,
            id=f"{application_ci}Secondary",
        )
        primary_bucket = BucketAttributes(
            bucket_name=f"{bucket_base_name}-{tag}us-east-2",
            region="us-east-2",
            account=self.account,
            id=f"{application_ci}Primary",
        )

        scratch_bucket_base_name = f"""{application_ci}-scratch-{app_environment}"""
        secondary_scratch_bucket = BucketAttributes(
            bucket_name=f"{scratch_bucket_base_name}-{tag}us-east-1",
            region="us-east-1",
            account=self.account,
            id=f"{application_ci}ScratchSecondary",
        )
        primary_scratch_bucket = BucketAttributes(
            bucket_name=f"{scratch_bucket_base_name}-{tag}us-east-2",
            region="us-east-2",
            account=self.account,
            id=f"{application_ci}ScratchPrimary",
        )

        primary_stack = RegionalStack(
            self,
            id="us-east-2",
            source_bucket=primary_bucket,
            target_buckets=[secondary_bucket],
            source_scratch_bucket=primary_scratch_bucket,
            target_scratch_buckets=[secondary_scratch_bucket],
            deploy_replication=deploy_replication,
            aws_environment=aws_cdk.Environment(
                account=account_ids[environment], region="us-east-2"
            ),
            application_ci=application_ci,
            tag=tag,
        )

        secondary_stack = RegionalStack(
            self,
            id="us-east-1",
            source_bucket=secondary_bucket,
            target_buckets=[primary_bucket],
            source_scratch_bucket=secondary_scratch_bucket,
            target_scratch_buckets=[primary_scratch_bucket],
            deploy_replication=deploy_replication,
            aws_environment=aws_cdk.Environment(
                account=account_ids[environment], region="us-east-1"
            ),
            application_ci=application_ci,
            tag=tag,
        )
