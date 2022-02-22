import time
from twitter_demographer.components import Component
import requests
import json
from twitter_demographer.components import not_null
from tqdm import tqdm

class PerspectiveScorer(Component):

    def __init__(self, api_key, attributes=None, wait_seconds=2, **kwargs):
        self.api_key = api_key
        if attributes is None:
            self.attributes = "TOXICITY,SEVERE_TOXICITY,IDENTITY_ATTACK,INSULT,PROFANITY,THREAT".split(",")
        else:
            self.attributes = attributes

        self.wait_seconds = wait_seconds
        super().__init__(**kwargs)

    def outputs(self):
        return [f"perspective_{k}" for k in self.attributes]

    def inputs(self):
        return ["text"]

    @not_null("text")
    def infer(self, data, *args):

        results = self.initialize_return_dict()

        pbar = tqdm(total=len(data), position=1)
        pbar.set_description("Running Toxicity API")
        for text in data["text"].values.tolist():
            pbar.update(1)

            try:
                dici = self.score(text)

                for index, values in dici.items():
                    results[f"perspective_{index}"].append(dici[index])
            except:
                for val in self.outputs():
                    results[val].append(None)

            time.sleep(self.wait_seconds)
        pbar.close()
        return results

    def score(self, text):
        headers = {
            'Content-Type': 'application/json',
        }

        params = (
            ('key', self.api_key),
        )

        data = {"comment": {"text": text}, "requestedAttributes": {}}

        for att in self.attributes:
            data["requestedAttributes"][att] = {}

        data = json.dumps(data)
        response = requests.post('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze', headers=headers,
                                 params=params, data=data)

        return {index: response.json()["attributeScores"][index]["summaryScore"]["value"] for index in self.attributes}


