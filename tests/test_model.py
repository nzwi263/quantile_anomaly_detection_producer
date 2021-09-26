######################################
#
# Title: test_model.py
# Purpose: Test set for model.py
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
import pytest
import json

from libs.models.model import Model
from libs.helpers.s3_helper import get_failed_assets_list


def test_model_batch_assets_payloads():
    assert 100 == len(Model(
        json.dumps(
            {
                "date": "01-09-2021"
            }
        )
    ).batch_assets_payloads())


def test_batch_queue_payloads():
    model = Model(
        json.dumps(
            {
                "date": "01-09-2021"
            }
        )
    )

    assetsBatches = model.batch_assets_payloads()

    assert 10 == len(model.batch_queue_payloads(assetsBatches))


def test_send_queue_payloads():
    assert 'Message accepted!' == Model(
        json.dumps(
            {
                "date": "01-09-2021"
            }
        )
    ).send_queue_payloads()


def test_retry_batch_assets_payloads():
    date = "01-08-2021"
    failedAssetsList = get_failed_assets_list(date)
    model = Model(
        json.dumps(
            {
                "date": date
            }
        )
    )

    assert 1 == len(
        model.retry_batch_assets_payloads(
            failedAssetsList
        )
    )


def test_retry_assets_history_fetch():
    assert 'Message accepted!' == Model(
        json.dumps(
            {
                "date": "01-08-2021"
            }
        )
    ).retry_assets_history_fetch()
