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

.. image:: https://colab.research.google.com/assets/colab-badge.svg
    :target: https://colab.research.google.com/drive/1nk532mQS1MDAu_J3FpVTxPg21C5r44SE?usp=sharing
    :alt: Open In Colab


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

    demo = Demographer()

    data = pd.DataFrame({"tweet_ids": ["1477976329710673921", "1467887350084689928", "1467887352647462912", "1290664307370360834", "1465284810696445952"]})

    component_one = Rehydrate(BEARER_TOKEN)
    component_two = GeoNamesDecoder(GEONAMES_TOKEN)
    component_three = HuggingFaceClassifier("cardiffnlp/twitter-roberta-base-sentiment")


    demo.add_component(component_one)
    demo.add_component(component_two)
    demo.add_component(component_three)

    print(demo.infer(data))

.. code-block:: python

                                             screen_name                created_at  ... geo_location_address cardiffnlp/twitter-roberta-base-sentiment
    1  ef51346744a099e011ff135f7b223186d4dab4d38bb1d8... 2021-12-06 16:03:10+00:00  ...                Milan                                         1
    4  146effc0d60c026197afe2404c4ee35dfb07c7aeb33720... 2021-11-29 11:41:37+00:00  ...                Milan                                         2
    2  ef51346744a099e011ff135f7b223186d4dab4d38bb1d8... 2021-12-06 16:03:11+00:00  ...                Milan                                         1
    0  241b67c6c698a70b18533ea7d4196e6b8f8eafd39afc6a... 2022-01-03 12:13:11+00:00  ...               Zurich                                         2
    3  df94741e2317dc8bfca7506f575ba3bd9a83deabfd9eec... 2020-08-04 15:02:04+00:00  ...            Viganello                                         2



Use-Case
--------

Say you want to use a custom classifier on some Twitter Data you have. For example, you might want to
detect the sentiment of the data using your own classifier.

.. code-block:: python

    class YourClassifier(Component):
        def __init__(self, model):
            self.model = model
            super().__init__()

        def inputs(self):
            return ["text"]

        def outputs(self):
            return [f"my_classifier"]

        # not null decorator helps you skip those record that have None in the field
        @not_null("text")
        def infer(self, data):

            return {"my_classifier": model.predict(data["text"])}

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

        @not_null("location")
        def infer(self, data):
            geo = self.initialize_return_dict()
            for val in data["location"]:
                    g = geocoder.geonames(val, key=self.key)
                    geo["geo_location_country"].append(g.country)
                    geo["geo_location_address"].append(g.address)
            return geo
Current Components
------------------

+------------------------------+-------------------------------------------------+
| Name                         |  Tool                                           |
+==============================+=================================================+
| Geolocation                  | GeoNames                                        |
+------------------------------+-------------------------------------------------+
| Sentiment / HateSpeech       | HuggingFace Models                              |
+------------------------------+--------------------------+----------------------+
| Demographics                 | M3Inference, FairFace Coming Soon               |
+------------------------------+--------------------------+----------------------+
| Topic Modeling               | Contextualized Topic Modeling                   |
+------------------------------+--------------------------+----------------------+

Limitations and Ethical Considerations
--------------------------------------

Inferring user attributes always carries the risk of compromising user privacy, while this process can be useful for
understanding and explaining phenomena in the social sciences, one should always consider the issues that this can create.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
