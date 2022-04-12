Components
==========

Twitter Rehydration
-------------------



GeoLocation
-----------

We currently embed two components for geolocation.

GeoNames
~~~~~~~~

One is based on the online endpoint provided by geonames.
This component is going to try to disambiguate the location field in user profiles

OpenStreetMap
~~~~~~~~~~~~~

The second component uses the OpenStreetMap endpoint. By default this is going to use the default online
server from OpenStreetMap.

.. code-block:: python

    NominatimDecoder(server_url="https://nominatim.openstreetmap.org/search")

However, this endpoint limits query to 1 per second.  You can download your local endpoint of open
street map and update the code as follows once ready:

.. code-block:: python

    NominatimDecoder(server_url="localhost:8889/search", sleep_time=0)

Demographics Attributes
-----------------------


M3 Inference Classifier

We are currently implementing another classifier based on the FairFace.

General Classification
----------------------

We support any HuggingFace classifier by default.


Word Counters
-------------

LIWC
~~~~

Twitter Demographer supports LIWC counters. The component assumes you have access to a LIWC dictionary.
Instantiating the component is very easy.

.. code-block:: python

    le = LIWCAnalyzer("liwc_file.dic")

The results on a single text should more or less look like this. Where each category of LIWC appears
as a column with the respective count.

.. code-block:: bash

                                text                                        screen_name  LIWC_A  LIWC_Bravo
    0  Any alpha bravo charlie Bravo  9f6ceda15ffa18bf2b27ec85880c6fa72a2ed139bb5d03...       2           2


Topic Modeling
--------------

We include CTM by default but we are working on adding additional text clustering methods for your data.
CTM can be used on multilingual data.

