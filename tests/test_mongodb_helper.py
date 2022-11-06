######################################
#
# Title: test_mongodb_helper.py
# Purpose: Test set for mongodb_helper.py
# Author: Nzwisisa Chidembo
# Date Created: 01 Nov 2022
# Date Updated: 01 Nov 2022
#
#######################################
import pytest
import json

from libs.models.model import Model
from libs.helpers.mongodb_helper import mongodb_find, mongodb_find_failed_assets


def test_mongodb_helper_mongodb_find():
    assert 3000 == len(mongodb_find(
        "2022-10-27",
        "2022-10-28"
    )['documents'])


def test_mongodb_helper_mongodb_find_failed_assets():
    assert 111 == len(mongodb_find_failed_assets(
        "2022-10-31",
        "2022-11-01"
    )['documents'])
