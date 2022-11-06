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
# from libs.helpers.s3_helper import get_assets_details, get_failed_assets_list, delete_failed_assets
from libs.helpers.sqs_helper import send_sqs_queue_payload
from libs.helpers.mongodb_helper import mongodb_find, mongodb_find_failed_assets

import logging
import json

from datetime import datetime, timedelta

from aws_xray_sdk.core import xray_recorder
import pandas as pd

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


class Model:

    def __init__(self, request):
        self.date = json.loads(request)['date']

    @xray_recorder.capture('model_get_dates')
    def get_dates(self):
        date_time_str = f'{self.date} 03:00:00'
        start_date_obj = datetime.strptime(
            date_time_str, '%d-%m-%Y %H:%M:%S')
        end_date_obj = start_date_obj + timedelta(days=1)

        start_date = start_date_obj.strftime("%Y-%m-%d")
        end_date = end_date_obj.strftime("%Y-%m-%d")

        return start_date, end_date

    @xray_recorder.capture('model_batch_assets_payloads')
    def batch_assets_payloads(self):
        try:
            # assetsDetails = get_assets_details()['Body']

            # assetsDetailsDf = pd.read_csv(assetsDetails)

            # calculate datetime strings for requested & +1 day requested

            # date_time_str = f'{self.date} 03:00:00'
            # start_date_obj = datetime.strptime(
            #     date_time_str, '%d-%m-%Y %H:%M:%S')
            # end_date_obj = start_date_obj + timedelta(days=1)

            # start_date = start_date_obj.strftime("%Y-%m-%d")
            # end_date = end_date_obj.strftime("%Y-%m-%d")

            start_date, end_date = self.get_dates()

            # print(f'model start_date / end_date : {start_date, end_date}')

            # reading from mongodb instead of s3
            coins_list = mongodb_find(start_date, end_date)['documents']

            # organise coins into batches of 500
            print(f'Length of coin_list: {len(coins_list)}')

            coinsBatches = []
            currentCoinsBatch = []

            for idx, coin in enumerate(coins_list):
                currentCoinsBatch.append(
                    {
                        "assetName": coin['id'],
                        "date": self.date
                    }
                )

                if (idx + 1) % 500 == 0:
                    coinsBatches.append(currentCoinsBatch)
                    currentCoinsBatch = []

            # assetsDetailsDf = assetsDetailsDf.set_index('id')

            # allAssetsList = list(assetsDetailsDf.index.values)

            # assetsBatches = []
            # currentAssetsBatch = []

            # for idx, asset in enumerate(allAssetsList):
            #     currentAssetsBatch.append(
            #         {
            #             "assetName": asset,
            #             "date": self.date
            #         }
            #     )

            #     if (idx + 1) % 30 == 0:
            #         assetsBatches.append(currentAssetsBatch)
            #         currentAssetsBatch = []
        except Exception as e:
            logger.exception(e)

        return coinsBatches

    @xray_recorder.capture('model_batch_queue_payloads')
    def batch_queue_payloads(self, assetsBatches):
        # queueRequestBatches = []
        currentQueueBatch = []
        currentQueueDelay = 0

        try:
            for idx, batch in enumerate(assetsBatches):
                currentQueueBatch.append(
                    {
                        "Id": str(idx),
                        "MessageBody": json.dumps(batch),
                        "DelaySeconds": currentQueueDelay * 180
                    }
                )

                currentQueueDelay += 1

                # if (idx + 1) % 10 == 0:
                #     queueRequestBatches.append(
                #         currentQueueBatch
                #     )
                #     currentQueueBatch = []
                #     currentQueueDelay = 0

                # if (idx + 1) == len(assetsBatches):
                #     if len(currentQueueBatch) != 0:
                #         queueRequestBatches.append(
                #             currentQueueBatch
                #         )
        except Exception as e:
            logger.exception(e)

        # # temp
        # with open(f'queueRequestBatches.json', 'w') as outfile:
        #     json.dump(queueRequestBatches, outfile)

        return currentQueueBatch

    @xray_recorder.capture('model_send_queue_payloads')
    def send_queue_payloads(self):

        try:
            assetsBatches = self.batch_assets_payloads()
            queueRequestBatches = self.batch_queue_payloads(assetsBatches)

            # queuesList = None
            # with open(f'{QUEUE_LIST_FILENAME}', 'r') as f:
            #     queuesList = json.loads(f.read())

            # for idx, queue in enumerate(queuesList):
            #     resp = send_sqs_queue_payload(
            #         queueRegion=queue['queue_region'],
            #         queueUrl=queue['queue_url'],
            #         queuePayload=queueRequestBatches[idx]
            #     )

            resp = send_sqs_queue_payload(
                queueRegion=SQS_QUEUE_REGION,
                queueUrl=SQS_QUEUE_URL,
                queuePayload=queueRequestBatches
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

                try:
                    # print('asset: ', asset)
                    currentAssetsBatch.append(
                        {
                            "assetName": asset['id'],
                            "date": self.date
                        }
                    )
                except Exception as e:
                    logger.exception(e)

                if (idx + 1) % 500 == 0:
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
            # failedAssetsList = get_failed_assets_list(self.date)
            # assetsBatches = self.retry_batch_assets_payloads(
            #     failedAssetsList)
            # queueRequestBatches = self.batch_queue_payloads(assetsBatches)

            # queuesList = None
            # with open(f'{QUEUE_LIST_FILENAME}', 'r') as f:
            #     queuesList = json.loads(f.read())

            # deleteCount = delete_failed_assets(failedAssetsList, self.date)

            # # logger.info('########### queueRequestBatches ###########')
            # # logger.info(queueRequestBatches)

            # for idx, queue in enumerate(queuesList):
            #     try:
            #         resp = send_sqs_queue_payload(
            #             queueRegion=queue['queue_region'],
            #             queueUrl=queue['queue_url'],
            #             queuePayload=queueRequestBatches[idx]
            #         )
            #     except Exception as e:
            #         logger.exception(e)

            start_date, end_date = self.get_dates()

            failed_coins = mongodb_find_failed_assets(
                start_date, end_date)['documents']
            # print('failed_coin[0]: ', failed_coins[0]['id'])
            failed_assets_batches = self.retry_batch_assets_payloads(
                failed_coins)

            queueRequestBatches = self.batch_queue_payloads(
                failed_assets_batches)

            # print('failed_assets_batches: ', queueRequestBatches)

            for queue in queueRequestBatches:
                try:
                    resp = send_sqs_queue_payload(
                        queueRegion=SQS_QUEUE_REGION,
                        queueUrl=SQS_QUEUE_URL,
                        queuePayload=[queue]
                    )
                except Exception as e:
                    logger.exception(e)

        except Exception as e:
            logger.exception(e)

        return 'Message accepted!'
