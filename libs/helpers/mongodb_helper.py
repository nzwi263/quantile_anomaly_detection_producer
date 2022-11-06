#######################################
#
# Title: mongodb_helper.py
# Purpose: MongoDB Data API helper
# Author: Nzwisisa Chidembo
# Date Created: 01 Nov 2022
# Date Updated: 01 Nov 2022
#
#######################################
from libs.helpers.constants_helper import *

import requests
import json
import logging

from aws_xray_sdk.core import xray_recorder


@xray_recorder.capture('mongodb_helper_mongodb_find')
def mongodb_find(start_date, end_date):
    message = None

    print('Data received in mongodb_find')
    print(f'start_date / end_date: {start_date} / {end_date}')

    try:
        url = MONGODB_RSKYCLUSTER_PLAYGROUND_URL + 'action/find'

        print('Beginning of payload formatting')

        payload = json.dumps({
            "dataSource": MONGODB_RSKYCLUSTER_DATA_SOURCE,
            "database": MONGODB_RSKYCLUSTER_DATABASE,
            "collection": MONGODB_RSKYCLUSTER_COINGECKO_TARGET_COINS_COLLECTION,
            "filter": {
                "timestamp": {"$gte": start_date, "$lt": end_date}
            },
            "sort": {"market_cap_rank": 1},
            "limit": 4000
        })

        print('End of payload formatting')

        headers = {
            'Content-Type': 'application/json',
            'api-key': MONGODB_RSKYCLUSTER_DATA_API_KEY
        }

        resp = requests.request("POST", url, headers=headers, data=payload)
        message = resp.text
    except Exception as e:
        logging.exception('Failed to get assets details page')
        message = [
            {
                'message': str(e)
            }
        ]

    return json.loads(message)


@xray_recorder.capture('mongodb_helper_mongodb_find_failed_assets')
def mongodb_find_failed_assets(start_date, end_date):
    message = None

    print('Data received in mongodb_find')
    print(f'start_date / end_date: {start_date} / {end_date}')

    try:
        url = MONGODB_RSKYCLUSTER_PLAYGROUND_URL + 'action/find'

        print('Beginning of payload formatting')

        payload = json.dumps({
            "dataSource": MONGODB_RSKYCLUSTER_DATA_SOURCE,
            "database": MONGODB_RSKYCLUSTER_DATABASE,
            "collection": MONGODB_RSKYCLUSTER_COINGECKO_COINS_HISTORY_FAILED_COLLECTION,
            "filter": {
                "timestamp": {"$gte": start_date, "$lt": end_date}
            },
            "limit": 4000
        })

        print('End of payload formatting')

        headers = {
            'Content-Type': 'application/json',
            'api-key': MONGODB_RSKYCLUSTER_DATA_API_KEY
        }

        resp = requests.request("POST", url, headers=headers, data=payload)
        message = resp.text
    except Exception as e:
        logging.exception('Failed to get assets details page')
        message = [
            {
                'message': str(e)
            }
        ]

    return json.loads(message)
