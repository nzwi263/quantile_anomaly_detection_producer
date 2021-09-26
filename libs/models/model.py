######################################
#
# Title: model.py
# Purpose: Main model for the project
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
from libs.helpers.constants_helper import *
from libs.helpers.s3_helper import get_assets_details, get_failed_assets_list, delete_failed_assets
from libs.helpers.sqs_helper import send_sqs_queue_payload

import logging
import json

from aws_xray_sdk.core import xray_recorder
import pandas as pd

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


class Model:

    def __init__(self, request):
        self.date = json.loads(request)['date']

    @xray_recorder.capture('model_batch_assets_payloads')
    def batch_assets_payloads(self):
        try:
            assetsDetails = get_assets_details()['Body']
            assetsDetailsDf = pd.read_csv(assetsDetails)

            assetsDetailsDf = assetsDetailsDf.set_index('id')

            allAssetsList = list(assetsDetailsDf.index.values)

            assetsBatches = []
            currentAssetsBatch = []

            for idx, asset in enumerate(allAssetsList):
                currentAssetsBatch.append(
                    {
                        "assetName": asset,
                        "date": self.date
                    }
                )

                if (idx + 1) % 30 == 0:
                    assetsBatches.append(currentAssetsBatch)
                    currentAssetsBatch = []
        except Exception as e:
            logger.exception(e)

        return assetsBatches

    @xray_recorder.capture('model_batch_queue_payloads')
    def batch_queue_payloads(self, assetsBatches):
        queueRequestBatches = []
        currentQueueBatch = []
        currentQueueDelay = 0

        try:
            for idx, batch in enumerate(assetsBatches):
                currentQueueBatch.append(
                    {
                        "Id": str(idx),
                        "MessageBody": json.dumps(batch),
                        "DelaySeconds": currentQueueDelay * 90
                    }
                )

                currentQueueDelay += 1

                if (idx + 1) % 10 == 0:
                    queueRequestBatches.append(
                        currentQueueBatch
                    )
                    currentQueueBatch = []
                    currentQueueDelay = 0

                if (idx + 1) == len(assetsBatches):
                    if len(currentQueueBatch) != 0:
                        queueRequestBatches.append(
                            currentQueueBatch
                        )
        except Exception as e:
            logger.exception(e)

        # # temp
        # with open(f'queueRequestBatches.json', 'w') as outfile:
        #     json.dump(queueRequestBatches, outfile)

        return queueRequestBatches

    @xray_recorder.capture('model_send_queue_payloads')
    def send_queue_payloads(self):

        try:
            assetsBatches = self.batch_assets_payloads()
            queueRequestBatches = self.batch_queue_payloads(assetsBatches)

            queuesList = None
            with open(f'{QUEUE_LIST_FILENAME}', 'r') as f:
                queuesList = json.loads(f.read())

            for idx, queue in enumerate(queuesList):
                resp = send_sqs_queue_payload(
                    queueRegion=queue['queue_region'],
                    queueUrl=queue['queue_url'],
                    queuePayload=queueRequestBatches[idx]
                )
        except Exception as e:
            logger.exception(e)

        return 'Message accepted!'

    @xray_recorder.capture('model_retry_batch_assets_payloads')
    def retry_batch_assets_payloads(self, failedAssetsList):
        try:
            assetsBatches = []
            currentAssetsBatch = []

            for idx, asset in enumerate(failedAssetsList):
                currentAssetsBatch.append(
                    {
                        "assetName": asset,
                        "date": self.date
                    }
                )

                if (idx + 1) % 30 == 0:
                    assetsBatches.append(currentAssetsBatch)
                    currentAssetsBatch = []

                if (idx + 1) == len(failedAssetsList):
                    if len(currentAssetsBatch) != 0:
                        assetsBatches.append(
                            currentAssetsBatch
                        )

        except Exception as e:
            logger.exception(e)

        return assetsBatches

    @xray_recorder.capture('model_retry_assets_history_fetch')
    def retry_assets_history_fetch(self):
        try:
            failedAssetsList = get_failed_assets_list(self.date)
            assetsBatches = self.retry_batch_assets_payloads(
                failedAssetsList)
            queueRequestBatches = self.batch_queue_payloads(assetsBatches)

            queuesList = None
            with open(f'{QUEUE_LIST_FILENAME}', 'r') as f:
                queuesList = json.loads(f.read())

            deleteCount = delete_failed_assets(failedAssetsList, self.date)

            # logger.info('########### queueRequestBatches ###########')
            # logger.info(queueRequestBatches)

            for idx, queue in enumerate(queuesList):
                try:
                    resp = send_sqs_queue_payload(
                        queueRegion=queue['queue_region'],
                        queueUrl=queue['queue_url'],
                        queuePayload=queueRequestBatches[idx]
                    )
                except Exception as e:
                    logger.exception(e)

        except Exception as e:
            logger.exception(e)

        return 'Message accepted!'
