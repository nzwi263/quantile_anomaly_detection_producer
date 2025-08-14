### quantile_anomaly_detection_producer

AWS Lambda producer that accepts HTTP POST requests and publishes the received payload to an Amazon SQS queue. It is intended to trigger downstream processing for quantile anomaly detection.

## Overview
- **Runtime**: Python 3.9
- **Framework**: Serverless Framework (AWS)
- **Entry point**: `handler.init_producer`
- **HTTP endpoint**: `POST /producer`
- **Action**: Sends a single-entry SQS batch with the request body as the `MessageBody`

## How it works
1. API Gateway invokes the Lambda `handler.init_producer` on `POST /producer`.
2. The handler parses `event.body` (must be JSON) and passes it to `libs.models.model.Model`.
3. `Model.process_request` sends a batch (size 1) to the configured SQS queue via `libs.helpers.sqs_helper.send_sqs_queue_payload`.
4. On success, the function returns HTTP 200 with `{ "message": "Successfully sent SQS queue payload" }`.
5. If `event.body` is missing, it returns HTTP 400.

## Project structure
- `handler.py`: Lambda entry point, validates input and orchestrates the call to the model
- `libs/models/model.py`: Core logic to build and send the SQS message
- `libs/helpers/sqs_helper.py`: Thin wrapper around `boto3` SQS `send_message_batch`
- `libs/helpers/constants_helper.py`: Centralized constants and environment variables
- `serverless.yml`: Deployment config, IAM, and HTTP event
- `tests/`: Unit/integration tests (see Testing section)

## Prerequisites
- Python 3.9
- Node.js 16+ and the Serverless Framework (`npm i -g serverless`)
- AWS account and credentials configured (e.g., via `aws configure`)
- Existing SQS queue (URL and region)

## Installation
```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Note: At runtime on AWS, `boto3` is provided via a Lambda layer. For local development/integration tests that hit AWS, you may want to `pip install boto3` in your virtualenv.

## Configuration
The function reads configuration from environment variables, which are wired via Serverless parameters in `serverless.yml`:

- `SQS_QUEUE_REGION` (required)
- `SQS_QUEUE_URL` (required)

You can pass these at deploy/invoke time using `--param` flags:
```bash
sls deploy \
  --param="AWS_REGION=eu-west-1" \
  --param="SQS_QUEUE_REGION=eu-west-1" \
  --param="SQS_QUEUE_URL=https://sqs.eu-west-1.amazonaws.com/123456789012/your-queue-name"
```

## Deployment
```bash
sls deploy \
  --param="AWS_REGION=<aws-region>" \
  --param="SQS_QUEUE_REGION=<aws-region>" \
  --param="SQS_QUEUE_URL=<your-sqs-queue-url>"
```

Serverless will provision:
- Lambda function `func` → `handler.init_producer`
- API Gateway route `POST /producer`
- IAM permissions to publish to SQS

## Invocation

### Deployed API
```bash
curl -X POST "https://<api-id>.execute-api.<region>.amazonaws.com/<stage>/producer" \
  -H 'Content-Type: application/json' \
  -d '[{"date": "2022-12-27"}]'
```

Expected response on success:
```json
{
  "message": "Successfully sent SQS queue payload"
}
```

### Local invoke (no API Gateway)
Provide the required environment variables and pass an event with a `body` string that is valid JSON.

```bash
export SQS_QUEUE_REGION=<aws-region>
export SQS_QUEUE_URL=<your-sqs-queue-url>

# Minimal event with a JSON string body
echo '{"body": "[{\"date\": \"2022-12-27\"}]"}' > event.json

sls invoke local -f func --path event.json
```

## Testing
This repository includes pytest-based tests.

```bash
pip install -r requirements.txt
pip install pytest boto3  # needed locally for AWS interactions
pytest -q
```

Notes:
- `tests/test_handler.py` invokes the handler with a simple event and expects a success message.
- `tests/test_sqs_helper.py` performs a real SQS call using `boto3` with a provided SQS URL. This is an integration test and requires valid AWS credentials and access to the target queue. Run with caution or skip it locally:
  - Run unit tests only: `pytest -k "not sqs_helper"`
  - Or set up a test queue and AWS creds before running.

## Troubleshooting
- HTTP 400 from the Lambda usually means `event.body` was missing or not provided.
- Ensure `SQS_QUEUE_URL` and `SQS_QUEUE_REGION` are set correctly and that the function IAM role has permission to publish to the queue.
- For local runs, confirm your environment has `boto3` and AWS credentials.

## Extending
- To enrich the message, update `libs/models/model.py` where `MessageBody` is constructed.
- To batch multiple messages per request, adjust the `Entries` list passed to `send_message_batch`.

