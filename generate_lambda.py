import json
import boto3
import datetime
import os

# Configure your Bedrock model ID (example: Amazon Titan)
MODEL_ID = "amazon.titan-text-lite-v1"  # Update if needed
BEDROCK_REGION = "us-east-1"  # Update based on your region

bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("ContentHistory")  # Make sure to create this table on AWS

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        keywords = body.get("keywords", "").strip()

        if not keywords:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Input keywords missing"})
            }

        # Prompt engineering
        prompt = f"Generate 5 creative marketing taglines or descriptions for: {keywords}"

        # Call Bedrock
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": prompt})
        )
        result = json.loads(response['body'].read())
        generated_text = result.get("results", [{}])[0].get("outputText", "No output generated.")

        # Save to DynamoDB
        item = {
            "HistoryId": str(datetime.datetime.utcnow().timestamp()),
            "Timestamp": datetime.datetime.utcnow().isoformat(),
            "InputKeywords": keywords,
            "GeneratedContent": generated_text,
            "ModelUsed": MODEL_ID
        }
        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"generated_content": generated_text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }