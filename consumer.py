"""
Script to simulate test-runner microservice that receives messages and stores results in DynamoDB
"""
import boto3
import json
import time
from decimal import Decimal

REGION = "us-west-2"
QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/202325946758/demo-queue"
TABLE_NAME = "demo-test-results"

sqs = boto3.client("sqs", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def process_message(message):
    """Simulate test execution and write result to DynamoDB"""
    body = json.loads(message["Body"])
    test_id = body["test_id"]
    test_name = body["test_name"]

    print(f"🚀 Running test suite: {test_name}")
    time.sleep(2)  # simulate a short test run
    result = {"status": "passed", "duration": 2.1}

    table.put_item(Item={
        "TestId": test_id,
        "TestName": test_name,
        "Result": result["status"],
        "Duration": Decimal(str(result["duration"])),
        "Timestamp": int(time.time())
    })
    print("🗂️ Result stored in DynamoDB")


def poll_queue():
    """Continuously poll SQS for messages until stopped manually"""
    print("📩 Polling SQS for messages...")
    try:
        while True:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5
            )

            messages = response.get("Messages", [])
            if not messages:
                print("No messages — waiting...")
                time.sleep(3)
                continue

            for message in messages:
                process_message(message)

                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                print("✅ Message processed and deleted\n")

    except KeyboardInterrupt:
        print("\n🛑 Stopping consumer gracefully...")


if __name__ == "__main__":
    poll_queue()
