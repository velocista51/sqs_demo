import boto3
import json
import uuid
import os

# Get region from environment variable
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/202325946758/demo-queue"

# boto3 will automatically use AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from environment
sqs = boto3.client("sqs", region_name=REGION)


def send_test_job():
    message = {
        "test_id": str(uuid.uuid4()),
        "test_name": "regression_suite_v1"
    }

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    print(f"✅ Sent test job {message['test_name']} with ID {message['test_id']}")
    print(f"Message ID: {response['MessageId']}")


if __name__ == "__main__":
    send_test_job()
