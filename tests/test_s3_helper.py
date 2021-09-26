######################################
#
# Title: test_s3_helper.py
# Purpose: Test set for s3_helper.py
# Author: Nzwisisa Chidembo
# Date Created: 23 Sept 2021
# Date Updated: 23 Sept 2021
#
#######################################
import pytest
import json

from libs.helpers.s3_helper import get_assets_details, get_failed_assets_list, delete_failed_assets, repopulate_failed_assets


def test_s3_helper_get_assets_details():
    assert 200 == get_assets_details()['ResponseMetadata']['HTTPStatusCode']


def test_s3_helper_get_failed_assets_list():
    assert 24 == len(get_failed_assets_list("24-09-2021"))


def test_s3_helper_delete_failed_assets():
    date = "25-09-2021"
    assetsList = get_failed_assets_list(date)

    assert len(assetsList) == delete_failed_assets(assetsList, date)


def test_s3_helper_repopulate_failed_assets():
    date = "01-08-2021"

    assetsList = None
    with open('failedAssetsList.json', 'r') as r:
        assetsList = json.loads(r.read())

    assert len(assetsList) == repopulate_failed_assets(assetsList, date)
