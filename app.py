#!/usr/bin/env python3

from aws_cdk import core

from secure_api_with_keys.stacks.back_end.unsecure_api_stack import UnSecureApiStack
from secure_api_with_keys.stacks.back_end.secure_api_with_keys_stack import SecureApiWithKeysStack

app = core.App()
# SecureApiWithKeysStack(app, "secure-api-with-keys")

# Deploy an unsecure public API
unsecure_api = UnSecureApiStack(
    app,
    "unsecure-api",
    stack_log_level="INFO",
    back_end_api_name="unsecure_public_api_01",
    description="Miztiik Automation: API Best Practice Demonstration. Secure-vs-UnSecure APIs. This stack deploys an unsecure public API"
)

# Secure your API by create private EndPoint to make it accessible from your VPCs
secure_api_with_keys = SecureApiWithKeysStack(
    app,
    "secure-api-with-keys",
    stack_log_level="INFO",
    back_end_api_name="secure_api_with_keys_01",
    description="Miztiik Automation: API Best Practice Demonstration. Secure-vs-UnSecure APIs. This stack deploys an API and secures it with API Keys & Usage Plans"
)

# Stack Level Tagging
core.Tag.add(app, key="Owner",
             value=app.node.try_get_context('owner'))
core.Tag.add(app, key="OwnerProfile",
             value=app.node.try_get_context('github_profile'))
core.Tag.add(app, key="GithubRepo",
             value=app.node.try_get_context('github_repo_url'))
core.Tag.add(app, key="Udemy",
             value=app.node.try_get_context('udemy_profile'))
core.Tag.add(app, key="SkillShare",
             value=app.node.try_get_context('skill_profile'))
core.Tag.add(app, key="AboutMe",
             value=app.node.try_get_context('about_me'))

app.synth()
