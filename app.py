#!/usr/bin/env python3

from aws_cdk import core

from secure_api_with_keys.secure_api_with_keys_stack import SecureApiWithKeysStack


app = core.App()
SecureApiWithKeysStack(app, "secure-api-with-keys")

app.synth()
