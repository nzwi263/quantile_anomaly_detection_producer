######################################
#
# Title: test_sqs_helper.py
# Purpose: Test set for sqs_helper.py
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
import pytest
import json

from libs.helpers.sqs_helper import send_sqs_queue_payload


def test_sqs_helper_send_sqs_queue_payload():
    assert 200 == send_sqs_queue_payload(
        queueRegion="eu-west-1",
        queueUrl="https://sqs.eu-west-1.amazonaws.com/139699787534/rq-quant-anomaly-detect-consumer--quantileAnomalyDetectionConsumerQ-HB9oRwyGltPf",
        queuePayload=[
            {
                "Id": "0",
                "MessageBody": json.dumps(
                    [
                        {
                            "date": "23-11-2022"
                        }
                    ]
                ),
                "DelaySeconds": 0
            }
        ]
    )["ResponseMetadata"]["HTTPStatusCode"]
