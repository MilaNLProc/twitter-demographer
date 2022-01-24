import hashlib
from tqdm import tqdm
import datetime
import json


class Demographer:
    """
    Main entry point of twitter-demographer.
    """

    def __init__(self, cache_steps=False):
        self.components = []
        self.cache_steps = cache_steps
        self.local_inputs = []

    def add_component(self, component):
        if len(self.components) == 0:
            self.components.append(component)
            self.local_inputs.extend(component.outputs() + component.inputs())  # first run we add both
        else:
            if set(component.inputs()) <= set(self.local_inputs):
                self.components.append(component)
            else:
                raise Exception("Some of the fields are not supported by this composition")

    def infer(self, data):
        pbar = tqdm(total=len(self.components), position=0)
        data = data.copy()
        pbar.set_description("Running Demographer")
        for component in self.components:

            update = component.infer(data)
            for key, value in update.items():
                data[key] = value

            if self.cache_steps:
                data.to_parquet("local.csv", engine="pyarrow")
            del component
            pbar.update(1)

            # add hash(y: str) because hash(x: int) = x
            data["screen_name"] = data["screen_name"].apply(
                lambda x: hashlib.sha3_256(str(hash(x) + hash("hash")).encode()).hexdigest())
        pbar.close()
        drop_keys = ['tweet_ids', 'name', 'user_id_str',
                     'user_id', 'id', 'profile_image_url', 'description']

        for key in drop_keys:
            del data[key]

        data = data.sample(frac=1)

        return data

    def get_versioned_json(self):
        json_dict = {"run_at": datetime.datetime.now().time(), "components" : []}

        for component in self.components:
            json_dict["components"].append({type(component).__name__ : component.__dict__})

        return json.dumps(json_dict)
