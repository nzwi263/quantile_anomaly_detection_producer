######################################
#
# Title: sqs_helper.py
# Purpose: AWS SQS helper to send batch queue payloads
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
from libs.helpers.constants_helper import *

import logging

from aws_xray_sdk.core import xray_recorder
import boto3

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


@xray_recorder.capture('sqs_helper_send_sqs_queue_payload')
def send_sqs_queue_payload(queueRegion, queueUrl, queuePayload):
    try:
        client = boto3.client('sqs', region_name=queueRegion)
        response = client.send_message_batch(
            QueueUrl=queueUrl,
            Entries=queuePayload
        )
    except Exception as e:
        logger.exception(e)

    return response
