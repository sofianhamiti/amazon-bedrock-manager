import json


def lambda_handler(event, context):
    print(event)
    auth_token = event["authorizationToken"]
    print(auth_token)
    effect = "Deny" if auth_token != "allow" else "Allow"

    response = {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": "*",
                }
            ],
        },
    }

    return response
