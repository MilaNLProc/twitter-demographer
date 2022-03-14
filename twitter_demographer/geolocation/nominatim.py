from tqdm import tqdm
import geocoder
from twitter_demographer.components import Component
import logging
from twitter_demographer.components import not_null

class NominatimDecoder(Component):
    """
    Wrappers on the geocoder API to disambiguate users' locations using nominatim from open street map
    """

    def __init__(self, server_url):
        super().__init__()
        self.server_url = server_url

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
            g = geocoder.osm(val, server_url=self.server_url).osm

            if "addr:country" in g:
                geo["nominatim_country"].append(g["addr:country"])

            if "addr:city" in g:
                geo["nominatim_city"].append(g["addr:city"])

            pbar.update(1)
        pbar.close()
        return geo
