#!/usr/bin/env python3

import aws_cdk as cdk

from root_env_stack import RootEnvStack

app_ci = "raa"

app = cdk.App()
branch = ""

RootEnvStack(
    app,
    id=f"""{app_ci}-datalake-{branch}dev""",
    application_ci=app_ci,
    cdk_boostrap_qualifier="base",
    # Remember...False, then True to avoid the deadlock...
    deploy_replication=False,
    app_environment="dev",
    environment="dev",
    credential_role_level="dev",
    tag=branch,
)

RootEnvStack(
    app,
    id=f"""{app_ci}-datalake-qa""",
    application_ci=app_ci,
    cdk_boostrap_qualifier="base",
    # Remember...False, then True to avoid the deadlock...
    deploy_replication=True,
    app_environment="qa",
    environment="qa",
    credential_role_level="dev",
    tag="",
)

RootEnvStack(
    app,
    id=f"""{app_ci}-datalake-prd""",
    application_ci=app_ci,
    cdk_boostrap_qualifier="base",
    # Remember...False, then True to avoid the deadlock...
    deploy_replication=True,
    app_environment="prd",
    environment="prd",
    credential_role_level="prd",
    tag="",
)
app.synth()
