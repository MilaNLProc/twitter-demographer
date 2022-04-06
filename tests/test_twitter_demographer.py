#!/usr/bin/env python

"""Tests for `twitter_demographer` package."""
import os

import pandas as pd
import pytest
from twitter_demographer import twitter_demographer
from twitter_demographer.geolocation.geonames import GeoNamesDecoder
from twitter_demographer.components import Rehydrate


def test_demographer():
    demo = twitter_demographer.Demographer()

    re = Rehydrate(os.getenv('TWEEPY_BEARER_TOKEN'))
    geo = GeoNamesDecoder(os.getenv('GEONAMES_API_KEY'))

    demo.add_component(re)
    demo.add_component(geo)

    print(demo.infer(pd.DataFrame({"tweet_ids": ["1477976329710673921"]})))

    # todo: need to find a way to test components, not sure github actions can support demanding computations


