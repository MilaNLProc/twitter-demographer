from tqdm import tqdm
import geocoder
from twitter_demographer.components import Component
import logging
from twitter_demographer.components import not_null
import time

class NominatimDecoder(Component):
    """
    Wrappers on the geocoder API to disambiguate users' locations using nominatim from open street map
    """

    def __init__(self, server_url="https://nominatim.openstreetmap.org/search", sleep_time=1.5):
        super().__init__()
        self.server_url = server_url
        self.sleep_time = sleep_time

    def outputs(self):
        return ["nominatim_city", "nominatim_country"]

    def inputs(self):
        return ["location"]

    @not_null("location")
    def infer(self, data):
        logger = logging.StreamHandler()
        logger.setLevel(logging.ERROR)
        geo = self.initialize_return_dict()
        pbar = tqdm(total=len(data), position=1)
        pbar.set_description("Geocoder")

        for val in data["location"]:

            if val is None:
                geo["nominatim_country"].append(None)
                geo["nominatim_city"].append(None)
            else:

                g = geocoder.osm(val, server_url=self.server_url).osm

                if "addr:country" in g:
                    geo["nominatim_country"].append(g["addr:country"])
                else:
                    geo["nominatim_country"].append(None)

                if "addr:city" in g:
                    geo["nominatim_city"].append(g["addr:city"])
                else:
                    geo["nominatim_city"].append(None)
                time.sleep(self.sleep_time)

            pbar.update(1)
        pbar.close()

        return geo
