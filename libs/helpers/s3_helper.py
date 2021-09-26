######################################
#
# Title: s3_helper.py
# Purpose: AWS S3 helper to fetch files
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
from libs.helpers.constants_helper import *

import logging
import json

from aws_xray_sdk.core import xray_recorder
import boto3
import pandas as pd

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


@xray_recorder.capture('s3_helper_get_assets_details')
def get_assets_details():
    obj = None
    try:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=TARGET_S3_BUCKET,
                            Key=TARGET_S3_ASSETS_DETAILS_PATH+TARGET_S3_ASSETS_DETAILS_FILENAME)
    except Exception as e:
        logger.exception(e)
    return obj


@xray_recorder.capture('s3_helper_get_failed_assets_list')
def get_failed_assets_list(date):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(TARGET_S3_BUCKET)

        # Fetch failed assets
        failedAssetsList = []

        for obj in bucket.objects.filter(Prefix=TARGET_S3_ASSETS_HISTORY_LEAD_PATH + date + TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH):
            failedAssetsList.append(obj.key[38:-5])

        # Fetch successful assets
        successfulAssetsList = []

        for obj in bucket.objects.filter(Prefix=TARGET_S3_ASSETS_HISTORY_LEAD_PATH + date + TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH):
            successfulAssetsList.append(obj.key[42:-5])

        # Fetch all assets
        assetsDetails = get_assets_details()['Body']
        assetsDetailsDf = pd.read_csv(assetsDetails)
        assetsDetailsDf = assetsDetailsDf.set_index('id')
        allAssetsList = list(assetsDetailsDf.index.values)

        # Find missing

        missingAssestList = list(set(allAssetsList).difference(
            successfulAssetsList + failedAssetsList))

        # Add missing assets to failed folder

        if len(missingAssestList) > 1:
            objCount = repopulate_failed_assets(missingAssestList, date)

        # logger.info(successfulAssetsList)

        # # temp
        # with open(f'failedAssetsList.json', 'w') as outfile:
        #     json.dump(failedAssetsList, outfile)
    except Exception as e:
        logger.exception(e)

    return failedAssetsList + missingAssestList


@xray_recorder.capture('s3_helper_delete_failed_assets')
def delete_failed_assets(assetsList, date):
    try:
        deleteCount = 0
        s3 = boto3.client('s3')

        objsToDelete = []
        for asset in assetsList:
            objsToDelete.append(
                {
                    'Key': TARGET_S3_ASSETS_HISTORY_LEAD_PATH + date + TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH + asset + '.json'
                }
            )
            deleteCount += 1

        s3.delete_objects(
            Bucket=TARGET_S3_BUCKET,
            Delete={
                'Objects': objsToDelete
            }
        )
    except Exception as e:
        logger.exception(e)

    return deleteCount


@xray_recorder.capture('s3_helper_repopulate_failed_assets')
def repopulate_failed_assets(assetsList, date):
    try:
        putCount = 0
        s3 = boto3.client('s3')
        obj = ['placeholder']

        for asset in assetsList:
            s3.put_object(
                Body=json.dumps(obj),
                Bucket=TARGET_S3_BUCKET,
                Key=TARGET_S3_ASSETS_HISTORY_LEAD_PATH + date +
                TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH + asset + '.json'
            )
            putCount += 1
    except Exception as e:
        logger.exception(e)

    return putCount
