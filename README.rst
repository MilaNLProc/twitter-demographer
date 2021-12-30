===================
Twitter Demographer
===================


.. image:: https://img.shields.io/pypi/v/twitter_demographer.svg
        :target: https://pypi.python.org/pypi/twitter_demographer

.. image:: https://img.shields.io/travis/vinid/twitter_demographer.svg
        :target: https://travis-ci.com/vinid/twitter_demographer

.. image:: https://readthedocs.org/projects/twitter-demographer/badge/?version=latest
        :target: https://twitter-demographer.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Twitter Demographer provides a simple API to enrich your twitter data with additional variables such as sentiment, user location,
gender and age. The tool is completely extensible and you can add your own components to the system.


* Free software: MIT license
* Documentation: https://twitter-demographer.readthedocs.io.


Features
--------

.. code-block:: python

    from twitter_demographer.twitter_demographer import Demographer
    from twitter_demographer.components import Rehydrate
    from twitter_demographer.demographics.m3 import GenderAndAge
    import pandas as pd

    bearer_token = "TWITTER BEARER"

    demo = Demographer()

    component_1 = Rehydrate(bearer_token)
    component_2 = GenderAndAge()

    # here are some tweet ids
    data = pd.DataFrame({"tweet_ids" : ["1431271570681606145", "1431271582861774854"]})

    demo.add_component(component_1) # we want to rehydrate the tweets first
    demo.add_component(component_2) # we want to predict (binary) gender and age then

    print(demo.infer(data))

.. code-block:: python

                 tweet_ids      screen_name              name user_id_str  ...                                               text    age gender   is_org
    0  1431271570681606145  federicobianchy  Federico Bianchi  2332157006  ...  🎉 #EMNLP2021 new paper! "SWEAT: Scoring Polari...  19-29   male  non-org
    1  1431271582861774854  federicobianchy  Federico Bianchi  2332157006  ...  SWEAT can be used on any pair of corpora! We u...  19-29   male  non-org

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
            pbar = tqdm(total=len(data))

            for val in data["location"]:
                pbar.update(1)
                if val is None:
                    geo["geo_location_country"].append(None)
                    geo["geo_location_address"].append(None)
                else:
                    g = geocoder.geonames(val, key=self.key)
                    geo["geo_location_country"].append(g.country)
                    geo["geo_location_address"].append(g.address)
            pbar.close()
            return geo

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
