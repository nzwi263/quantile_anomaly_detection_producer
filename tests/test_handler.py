######################################
#
# Title: test_handler.py
# Purpose: Test set for handler.py
# Author: Nzwisisa Chidembo
# Date Created: 19 Sept 2021
# Date Updated: 26 Sept 2021
#
#######################################

import pytest
import json

# from handler import init_producer, init_retry
from handler import init_producer


def test_handler_init_producer():
    assert {'body': '{"message": "Message accepted!"}', 'statusCode': 200} == init_producer(
        {
            "body": json.dumps(
                {
                    "date": "25-09-2021"
                }
            )
        },
        []
    )


# def test_handler_init_retry():
#     assert {'body': '{"message": "Message accepted!"}', 'statusCode': 200} == init_retry(
#         {
#             "body": json.dumps(
#                 {
#                     "date": "25-09-2021"
#                 }
#             )
#         },
#         []
#     )
