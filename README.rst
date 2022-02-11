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


.. image:: https://raw.githubusercontent.com/MilaNLProc/twitter-demographer/main/img/twitter-demographer.gif
   :width: 600pt


* Free software: MIT license
* Documentation: https://twitter-demographer.readthedocs.io.

**Note** the API is still under development (e.g., we have a lot of logging going on behind the scene) feel free to
suggest improvements or submit PRs! We are also working on improving the documentation and adding more examples!

Features
--------

From a simple set of tweet ids, Twitter Demographer allows you to rehydrate them and to add additional
variables to your dataset.

You are not forced to use a specific component. The design of this tool should be modular enough to allow you to
decide what to add and what to remove.

Let's make an example: you have a set of tweet ids (from english speakers) and you want to:

+ reconstruct the original tweets
+ disambiugate the location of the users
+ predict the sentiment of the tweet.

This can be done with very few lines of code with this library.

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

Note that you still need to register to both twitter developer and to geonames to use the services.

Privacy Matters
---------------

Following the recommendations of the EU's General Data Protection Regulation, we implement a variety of measures to ensure pseudo-anonymity by design. Using \tool provides several built-in measures to remove identifying information and protect user privacy:

+ removing identifiers
+ unidirectional hashing
+ aggregate label swapping.

This does not compromise the value of aggregated analysis but allows for a fairer usage of this data.

Extending
---------

However, the library is also extensible. Say you want to use a custom classifier on some Twitter Data you have. For example, you might want to
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

The project and the components are still under development and we are working on introducing novel pipelines to support
different use-cases.

You can see the components currently integrated in the system `here <https://twitter-demographer.readthedocs.io/en/latest/components.html>`__

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

Twitter Demographer does not come without limitations.
Some of these are related to the precision of the components used; for example, the Geonames decoder can fail the disambiguation - even if it has been adopted by other researchers and services. At the same time, the the topic modeling pipeline can be affected by the number of tweets used to train the model and by other training issues (fixing random seeds can generate suboptimal solutions).

The tool wraps the API from M3 for age and gender prediction. However, those predictions for gender are binary (male or female) and thus give a stereotyped representation of gender. Our intent is not to make normative claims about gender, as this is far from our beliefs. Twitter Demographer allows using other, more flexible tools. The API needs both text and user profile pictures of a tweet to make inferences, for that reason the tool has to include such information in the dataset during the pipeline execution. While this information is public (e.g., user profile pictures), the final dataset contains also inferred information, which may not be publicly available (e.g., gender or age of the user). We cannot completely prevent misuse of this capability but have taken steps to substantially reduce the risk and promote privacy by design.

Inferring user attributes carries the risk of privacy violations. We follow the definitions and recommendations of the European Union's General Data Protection Regulation for algorithmic pseudo-anonymity. We implement several measures to break a direct mapping between attributes and identifiable users without reducing the generalizability of aggregate findings on the data.
Our measures follow the GDPR definition of a "motivated intruder", i.e., it requires "significant effort" to undo our privacy protection measures. However, given enough determination and resources, a bad actor might still be able to circumvent or reverse-engineer these measures. This is true independent of Twitter Demographer, though, as existing tools could be used more easily to achieve those goals.
Using the tool provides practitioners with a reasonable way to protect anonymity.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
