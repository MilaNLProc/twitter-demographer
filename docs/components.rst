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


Topic Modeling
--------------

We include CTM by default but we are working on adding additional text clustering methods for your data.
CTM can be used on multilingual data.

