from tqdm import tqdm
import geocoder
from twitter_demographer.components import Component
import logging



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

    def infer(self, data):
        logger = logging.StreamHandler()
        logger.setLevel(logging.ERROR)
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
