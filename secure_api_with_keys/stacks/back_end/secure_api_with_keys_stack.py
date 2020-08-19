from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_secretsmanager as _secretsmanager

import json
from aws_cdk import core

import os


class GlobalArgs:
    """
    Helper to define global statics
    """

    OWNER = "MystiqueAutomation"
    ENVIRONMENT = "production"
    REPO_NAME = "secure-api-with-keys"
    SOURCE_INFO = f"https://github.com/miztiik/{REPO_NAME}"
    VERSION = "2020_08_18"
    MIZTIIK_SUPPORT_EMAIL = ["mystique@example.com", ]


class SecureApiWithKeysStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        stack_log_level: str,
        back_end_api_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Serverless Event Processor using Lambda):
        # Read Lambda Code):
        try:
            with open("secure_api_with_keys/stacks/back_end/lambda_src/serverless_greeter.py", mode="r") as f:
                greeter_fn_code = f.read()
        except OSError as e:
            print("Unable to read Lambda Function Code")
            raise e

        greeter_fn = _lambda.Function(
            self,
            "secureGreeterFn",
            function_name=f"greeter_fn_{id}",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(greeter_fn_code),
            timeout=core.Duration.seconds(15),
            reserved_concurrent_executions=20,
            environment={
                "LOG_LEVEL": f"{stack_log_level}",
                "Environment": "Production",
                "ANDON_CORD_PULLED": "False",
                "RANDOM_SLEEP_ENABLED": "False"
            },
            description="Creates a simple greeter function"
        )
        greeter_fn_version = greeter_fn.latest_version
        greeter_fn_version_alias = _lambda.Alias(
            self,
            "greeterFnAlias",
            alias_name="MystiqueAutomation",
            version=greeter_fn_version
        )

        # Create Custom Loggroup
        # /aws/lambda/function-name
        greeter_fn_lg = _logs.LogGroup(
            self,
            "greeterFnLoggroup",
            log_group_name=f"/aws/lambda/{greeter_fn.function_name}",
            retention=_logs.RetentionDays.ONE_WEEK,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Add API GW front end for the Lambda
        back_end_01_api_stage_options = _apigw.StageOptions(
            stage_name="miztiik",
            throttling_rate_limit=10,
            throttling_burst_limit=100,
            # Log full requests/responses data
            data_trace_enabled=True,
            # Enable Detailed CloudWatch Metrics
            metrics_enabled=True,
            logging_level=_apigw.MethodLoggingLevel.INFO,
        )

        # Create API Gateway
        secure_api_with_keys_01 = _apigw.RestApi(
            self,
            "backEnd01Api",
            rest_api_name=f"{back_end_api_name}",
            deploy_options=back_end_01_api_stage_options,
            endpoint_types=[
                _apigw.EndpointType.REGIONAL
            ],
            description=f"{GlobalArgs.OWNER}: API Best Practice Demonstration - Security for APIs with Keys"
        )

        # Start with the API Keys
        dev_kon_api_key = _apigw.ApiKey(
            self,
            "devApiKey",
            description="The Api Key for 'Kon' Developer",
            enabled=True,
            api_key_name="Developer-Kon-Key",
            # value ="" # Leave it to AWS to create a random key for us
        )

        partner_api_key = _apigw.ApiKey(
            self,
            "partnerApiKey",
            description="The Api Key for 'Partner' Mystique Corp",
            enabled=True,
            api_key_name="Partner-Mystique-Corp-Key",
        )

        # We have API Keys to attach to Usage Plan

        secure_api_with_keys_01_usage_plan_01 = secure_api_with_keys_01.add_usage_plan(
            "secureApiDevUsagePlan",
            name="DeveloperUsagePlan",
            api_key=dev_kon_api_key,
            api_stages=[
                _apigw.UsagePlanPerApiStage(
                    api=secure_api_with_keys_01,
                    stage=secure_api_with_keys_01.deployment_stage
                )
            ],
            throttle=_apigw.ThrottleSettings(
                burst_limit=1,
                rate_limit=1
            ),
            description="Api Security with usage plan and throttling"
        )
        secure_api_with_keys_01_usage_plan_02 = secure_api_with_keys_01.add_usage_plan(
            "secureApiPartnerUsagePlan",
            name="PartnerUsagePlan",
            api_key=partner_api_key,
            api_stages=[
                _apigw.UsagePlanPerApiStage(
                    api=secure_api_with_keys_01,
                    stage=secure_api_with_keys_01.deployment_stage
                )
            ],
            throttle=_apigw.ThrottleSettings(
                burst_limit=100,
                rate_limit=10
            ),
            description="Mystique Automation: Api Security with usage plan and throttling. Usage plan for Partner Mystique Corp"
        )

        back_end_01_api_res = secure_api_with_keys_01.root.add_resource(
            "secure")
        greeter = back_end_01_api_res.add_resource("greeter")

        greeter_method_get = greeter.add_method(
            http_method="GET",
            request_parameters={
                "method.request.header.InvocationType": True,
                "method.request.path.pkon": True
            },
            integration=_apigw.LambdaIntegration(
                handler=greeter_fn,
                proxy=True
            ),
            api_key_required=True
        )

        # Outputs
        output_1 = core.CfnOutput(
            self,
            "SecureApiWithKeysUrl",
            value=f"{greeter.url}",
            description="Use an utility like curl from the same VPC as the API to invoke it."
        )
