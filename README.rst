===================
Twitter Demographer
===================


.. image:: https://img.shields.io/pypi/v/twitter-demographer.svg
        :target: https://pypi.python.org/pypi/twitter-demographer

.. image:: https://github.com/MilaNLProc/twitter-demographer/workflows/Python%20package/badge.svg
        :target: https://github.com/MilaNLProc/twitter-demographer/actions

.. image:: https://readthedocs.org/projects/twitter-demographer/badge/?version=latest
        :target: https://twitter-demographer.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Twitter Demographer provides a simple API to enrich your twitter data with additional variables such as sentiment, user location,
gender and age. The tool is completely extensible and you can add your own components to the system.


* Free software: MIT license
* Documentation: https://twitter-demographer.readthedocs.io.


Features
--------

From a simple set of tweet ids, Twitter Demographer allows you to rehydrate them and to add additional
variables to your dataset.

You are not forced to use a specific component. The design of this tool should be modular enough to allow you to
decide what to add and what to remove.

.. code-block:: python

    from twitter_demographer.twitter_demographer import Demographer
    from twitter_demographer.components import Rehydrate
    from twitter_demographer.demographics.m3 import GenderAndAge
    import pandas as pd

    twitter_bearer_token = "TWITTER BEARER"
    geonames_token = "GEONAMES TOKEN"

    demo = Demographer()

    component_1 = Rehydrate(twitter_bearer_token)
    component_2 = GeoNamesDecoder(geonames_token)
    component_3 = GenderAndAge()

    data = pd.DataFrame({"tweet_ids": ["1431271582861774854", "1467887357668077581",
                                       "1467887350084689928", "1467887352647462912"]})
    print(data)
    demo.add_component(component_1)
    demo.add_component(component_2)
    demo.add_component(component_3)

    print(demo.infer(data))

.. code-block:: python

                 tweet_ids      screen_name              name           location user_id_str  ...  geo_location_country  geo_location_address    age gender   is_org
    0  1431271582861774854  federicobianchy  Federico Bianchi  Milano, Lombardia  2332157006  ...                 Italy                 Milan  19-29   male  non-org
    1  1467887357668077581  federicobianchy  Federico Bianchi  Milano, Lombardia  2332157006  ...                 Italy                 Milan  19-29   male  non-org
    2  1467887350084689928  federicobianchy  Federico Bianchi  Milano, Lombardia  2332157006  ...                 Italy                 Milan  19-29   male  non-org
    3  1467887352647462912  federicobianchy  Federico Bianchi  Milano, Lombardia  2332157006  ...                 Italy                 Milan  19-29   male  non-org

Use-Case
--------

Say you want to use an HuggingFace Classifier on some Twitter Data you have. For example, you might want to
detect the sentiment of the data you have.

Components
----------

Twitter Demographer is based on components that can be concatenated together to build tools. For example, the
GeoNamesDecoder to predict the location of a user from a string of text looks like this.

.. code-block:: python

    class GeoNamesDecoder(Component):

        def __init__(self, key):
            super().__init__()
            self.key = key

        def outputs(self):
            return ["geo_location_country", "geo_location_address"]

        def inputs(self):
            return ["location"]

        def infer(self, data):
            geo = self.initialize_return_dict()
            for val in data["location"]:
                if val is None:
                    geo["geo_location_country"].append(None)
                    geo["geo_location_address"].append(None)
                else:
                    g = geocoder.geonames(val, key=self.key)
                    geo["geo_location_country"].append(g.country)
                    geo["geo_location_address"].append(g.address)
            return geo

Limitations and Ethical Considerations
--------------------------------------



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
