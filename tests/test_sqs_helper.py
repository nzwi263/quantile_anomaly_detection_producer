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
        queueRegion="us-east-1",
        queueUrl="https://sqs.us-east-1.amazonaws.com/828366613602/riskbloq-ahf-dev-assetsHistoryQueue-1A57NWP7PAUK3",
        queuePayload=[
            {
                "Id": "0",
                "MessageBody": json.dumps(
                    [
                        {
                            "assetName": "bitcoin",
                            "date": "01-09-2021"
                        }
                    ]
                ),
                "DelaySeconds": 0
            }
        ]
    )["ResponseMetadata"]["HTTPStatusCode"]
