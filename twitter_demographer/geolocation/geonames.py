from tqdm import tqdm
import geocoder
from twitter_demographer.components import Component
import logging
from twitter_demographer.components import not_null

class GeoNamesDecoder(Component):
    """
    Wrappers on the geocoder API to disambiguate users' locations
    """

    def __init__(self, key):
        super().__init__()
        self.key = key

    def outputs(self):
        return ["geo_location_country", "geo_location_address"]

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
            g = geocoder.geonames(val, key=self.key)
            geo["geo_location_country"].append(g.country)
            geo["geo_location_address"].append(g.address)
            pbar.update(1)
        pbar.close()
        return geo
