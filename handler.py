######################################
#
# Title: handler.py
# Purpose: Entry file to function
# Author: Nzwisisa Chidembo
# Date Created: 19 Sept 2021
# Date Updated: 26 Sept 2021
#
#######################################
from libs.helpers.constants_helper import *
from libs.models.model import Model

import json
import logging

from aws_xray_sdk.core import xray_recorder

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


@xray_recorder.capture('handler_init_producer')
def init_producer(event, context):
    status_code = 200
    message = ''

    if not event.get('body'):
        return {'statusCode': 400, 'body': json.dumps({'message': 'No body was found'})}

    try:
        logger.info(event)
        message = 'Exposing API Gateway Payload'
        if event['path'] == '/producer':
            message = Model(event['body']).send_queue_payloads()
        elif event['path'] == '/retry':
            message = Model(event['body']).retry_assets_history_fetch()
    except Exception as e:
        logger.exception('Sending message to SQS queue failed!')
        message = str(e)
        status_code = 500

    return {'statusCode': status_code, 'body': json.dumps({'message': message})}
