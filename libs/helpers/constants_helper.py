######################################
#
# Title: constants_helper.py
# Purpose: Project wide constants
# Author: Nzwisisa Chidembo
# Date Created: 26 Dec 2022
# Date Updated: 26 Dec 2022
#
#######################################
import logging
import os

# Logging
LOG_LEVEL = logging.INFO

# model.py
SQS_QUEUE_REGION = os.getenv('SQS_QUEUE_REGION', 'not_provided')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', 'not_provided')
