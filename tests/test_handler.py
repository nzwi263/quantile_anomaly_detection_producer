######################################
#
# Title: test_handler.py
# Purpose: Test set for handler.py
# Author: Nzwisisa Chidembo
# Date Created: 26 Dec 2022
# Date Updated: 26 Dec 2022
#
#######################################

import pytest
import json

from handler import init_producer


def test_handler_init_producer():
    assert {'body': '{"message": "Successfully sent SQS queue payload"}', 'statusCode': 200} == init_producer(
        {
            "body": json.dumps(
                [
                    {
                        "date": "27-12-2022"
                    }
                ]
            )
        },
        []
    )