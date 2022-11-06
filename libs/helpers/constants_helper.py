######################################
#
# Title: constants_helper.py
# Purpose: Project wide constants
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
import logging
import os

# Logging
LOG_LEVEL = logging.INFO

# mongodb_helper.py
MONGODB_RSKYCLUSTER_REGION = os.getenv(
    'MONGODB_RSKYCLUSTER_REGION', 'not_provided')
MONGODB_RSKYCLUSTER_DATA_API_APP_ID = os.getenv(
    'MONGODB_RSKYCLUSTER_DATA_API_APP_ID', 'not_provided')
MONGODB_RSKYCLUSTER_DATA_API_KEY = os.getenv(
    'MONGODB_RSKYCLUSTER_DATA_API_KEY', 'not_provided')
MONGODB_RSKYCLUSTER_PLAYGROUND_URL = f'https://{MONGODB_RSKYCLUSTER_REGION}.aws.data.mongodb-api.com/app/{MONGODB_RSKYCLUSTER_DATA_API_APP_ID}/endpoint/data/v1/'
MONGODB_RSKYCLUSTER_DATA_SOURCE = os.getenv(
    'MONGODB_RSKYCLUSTER_DATA_SOURCE', 'not_provided')
MONGODB_RSKYCLUSTER_DATABASE = os.getenv(
    'MONGODB_RSKYCLUSTER_DATABASE', 'not_provided')
MONGODB_RSKYCLUSTER_COINGECKO_TARGET_COINS_COLLECTION = os.getenv(
    'MONGODB_RSKYCLUSTER_COINGECKO_TARGET_COINS_COLLECTION', 'not_provided')
MONGODB_RSKYCLUSTER_COINGECKO_COINS_HISTORY_FAILED_COLLECTION = os.getenv(
    'MONGODB_RSKYCLUSTER_COINGECKO_COINS_HISTORY_FAILED_COLLECTION', 'not_provided')

# # s3_helper.py
# TARGET_S3_BUCKET = os.getenv('TARGET_S3_BUCKET', 'not_provided')
# TARGET_S3_ASSETS_DETAILS_PATH = os.getenv(
#     'TARGET_S3_ASSETS_DETAILS_PATH', 'not_provided')
# TARGET_S3_ASSETS_DETAILS_FILENAME = os.getenv(
#     'TARGET_S3_ASSETS_DETAILS_FILENAME', 'not_provided')
# TARGET_S3_ASSETS_HISTORY_LEAD_PATH = os.getenv(
#     'TARGET_S3_ASSETS_HISTORY_LEAD_PATH', 'not_provided')
# TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH = os.getenv(
#     'TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH', 'not_provided')
# TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH = os.getenv(
#     'TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH', 'not_provided')

# # model.py
# QUEUE_LIST_FILENAME = os.getenv('QUEUE_LIST_FILENAME', 'not_provided')

# model.py
SQS_QUEUE_REGION = os.getenv('SQS_QUEUE_REGION', 'not_provided')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', 'not_provided')
