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

# s3_helper.py
TARGET_S3_BUCKET = os.getenv('TARGET_S3_BUCKET', 'not_provided')
TARGET_S3_ASSETS_DETAILS_PATH = os.getenv(
    'TARGET_S3_ASSETS_DETAILS_PATH', 'not_provided')
TARGET_S3_ASSETS_DETAILS_FILENAME = os.getenv(
    'TARGET_S3_ASSETS_DETAILS_FILENAME', 'not_provided')
TARGET_S3_ASSETS_HISTORY_LEAD_PATH = os.getenv(
    'TARGET_S3_ASSETS_HISTORY_LEAD_PATH', 'not_provided')
TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH = os.getenv(
    'TARGET_S3_ASSETS_HISTORY_FAILED_TAIL_PATH', 'not_provided')
TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH = os.getenv(
    'TARGET_S3_ASSETS_HISTORY_SUCCESSFUL_TAIL_PATH', 'not_provided')

# model.py
QUEUE_LIST_FILENAME = os.getenv('QUEUE_LIST_FILENAME', 'not_provided')
