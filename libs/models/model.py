######################################
#
# Title: model.py
# Purpose: Main model for the project
# Author: Nzwisisa Chidembo
# Date Created: 26 Dec 2022
# Date Updated: 26 Dec 2022
#
#######################################
from libs.helpers.constants_helper import *
from libs.helpers.sqs_helper import send_sqs_queue_payload

import logging
import json

# from aws_xray_sdk.core import xray_recorder

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


class Model:

    def __init__(self, request):
        self.request = json.loads(request)

    # @xray_recorder.capture('model_process_request')
    def process_request(self):
        logger.info('Starting to process request')
        message = ''
        try:
            response = send_sqs_queue_payload(
                queueRegion=SQS_QUEUE_REGION,
                queueUrl=SQS_QUEUE_URL,
                queuePayload=[
                    {
                        "Id": "0",
                        "MessageBody": json.dumps(self.request),
                        "DelaySeconds": 0
                    }
                ]
            )

            logger.info(response)
            logger.info('Successfully sent SQS queue payload')
            message = 'Successfully sent SQS queue payload'
        except Exception as e:
            message = str(e)
            logger.exception(e)
            raise Exception('Failed to send SQS queue payload')

        return message