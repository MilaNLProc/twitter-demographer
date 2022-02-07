#!/usr/bin/env python

"""Tests for `twitter_demographer` package."""

import pytest
from twitter_demographer import twitter_demographer
from twitter_demographer.geolocation.geonames import GeoNamesDecoder
from twitter_demographer.components import Rehydrate

def test_demographer():
    demo = twitter_demographer.Demographer()

    re = Rehydrate("test")
    geo = GeoNamesDecoder("gege")

    demo.add_component(re)
    demo.add_component(geo)

    # todo: need to find a way to test components, not sure github actions can support demanding computations


