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




Twitter Demographer


* Free software: MIT license
* Documentation: https://twitter-demographer.readthedocs.io.


Features
--------

.. code-block:: python

    from twitter_demographer.twitter_demographer import Demographer
    from twitter_demographer.components import Rehydrate, M3GenderAndAge
    import pandas as pd

    bearer_token = "TWITTER BEARER"

    demo = Demographer()

    component_1 = Rehydrate(bearer_token, [])
    component_2 = M3GenderAndAge()

    # here's some tweet id
    data = pd.DataFrame({"tweet_ids" : ["1431271570681606145", "1431271582861774854"]})

    demo.add_component(component_1) # we want to rehydrate the tweets first
    demo.add_component(component_2) # we want to predict (binary) gender and age then

    print(demo.infer(data))

.. code-block:: python

                 tweet_ids      screen_name              name user_id_str  ...                                               text    age gender   is_org
    0  1431271570681606145  federicobianchy  Federico Bianchi  2332157006  ...  🎉 #EMNLP2021 new paper! "SWEAT: Scoring Polari...  19-29   male  non-org
    1  1431271582861774854  federicobianchy  Federico Bianchi  2332157006  ...  SWEAT can be used on any pair of corpora! We u...  19-29   male  non-org



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
