import json
import os
import boto3

os.environ["AWS_PROFILE"] = "ravi"

boto3_bedrock = boto3.client(service_name="bedrock-runtime", region_name='us-west-2')
prompt = "hello"
modelId = "mistral.mixtral-8x7b-instruct-v0:1"
body = {
    "prompt": f"{prompt}",
    "max_tokens": 512,
    "top_k": 200,
    "top_p": 0.9,
    "stop": [],
    "temperature": 0.5
}

response = boto3_bedrock.invoke_model(modelId=modelId, body=json.dumps(body))
resp_body = json.loads(response.get("body").read())
print(resp_body)
