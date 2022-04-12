#!/usr/bin/env python

"""Tests for `twitter_demographer` package."""

import pytest
import os
from twitter_demographer import twitter_demographer
from twitter_demographer.geolocation.nominatim import NominatimDecoder
from twitter_demographer.components import Rehydrate
import pandas as pd
from twitter_demographer.analyzer.liwc import LIWCAnalyzer

def test_demographer():
    demo = twitter_demographer.Demographer()
    data = pd.DataFrame({"tweet_ids": ["1477976329710673921", "1467887350084689928"]})

    re = Rehydrate(os.getenv('TWEEPY_BEARER_TOKEN'))
    geo = NominatimDecoder()

    demo.add_component(re)
    demo.add_component(geo)

    demo.infer(data)

def test_liwc():
    """
    For this test we replicate the test run by the package liwc-python
    :return:
    """
    demo = twitter_demographer.Demographer()
    le = LIWCAnalyzer("tests/alpha.dic")

    data = pd.DataFrame(
        {"text": ["Any alpha bravo charlie Bravo"], "screen_name": ["a"], "tweet_ids": [1], "name": ["k"],
         "user_id_str": [12], "user_id": [12], "id": [12], "profile_image_url": ["hht"], "description": ["asdafs"]})

    demo.add_component(le)

    data = demo.infer(data)

    assert data["LIWC_A"].values[0] == 2
    assert data["LIWC_Bravo"].values[0] == 2


