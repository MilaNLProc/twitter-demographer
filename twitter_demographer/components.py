import abc

import pandas as pd
from tqdm import tqdm
import tweepy
from tweepy.errors import BadRequest
import transformers
from collections import defaultdict
from abc import ABC

transformers.logging.set_verbosity(transformers.logging.ERROR)

class Component(ABC):

    def __init__(self):
        self.output_parameters = self.outputs()

    @abc.abstractmethod
    def outputs(self):
        pass

    @abc.abstractmethod
    def inputs(self):
        pass

    @abc.abstractmethod
    def infer(self, *args):
        pass

    def initialize_return_dict(self):
        """
        A simple function that creates a dictionary with keys = parameters and values empty lists
        :return:
        """
        results = {}

        for param in self.output_parameters:
            results[param] = []
        return results


class Rehydrate(Component):

    def __init__(self, bearer_token):
        """
        :param bearer_token: token from the twitter developer page
        """
        super().__init__()
        self.api = tweepy.Client(bearer_token, wait_on_rate_limit=True)

    def inputs(self):
        return ["tweet_ids"]

    def outputs(self):
        return ['screen_name', 'name', 'location', 'user_id_str',
                'user_id', 'id', 'profile_image_url', 'description',
                'created_at', 'text']

    def infer(self, data):
        results = self.initialize_return_dict()

        pbar = tqdm(total=len(data))
        for tweet_id in data["tweet_ids"]:
            try:
                requested = self.api.get_tweet(tweet_id,
                                               tweet_fields=[
                                                   'id', 'text', 'author_id', 'created_at', 'conversation_id',
                                                   'entities',
                                                   'public_metrics', 'referenced_tweets'
                                               ],
                                               expansions=[
                                                   'author_id', 'referenced_tweets.id',
                                                   'referenced_tweets.id.author_id',
                                               ],
                                               place_fields=['full_name', 'id'],
                                               user_fields=[
                                                   'id', 'name', 'username', 'profile_image_url', 'description',
                                                   'location'
                                               ])
            except BadRequest as e:
                pbar.update(1)
                for key in self.outputs():
                    results[key].append(None)
                continue

            pbar.update(1)
            pbar.set_description("Running Hydrate")

            tweet = requested[0]
            if (len(requested.errors)) > 0:
                # if there are errors, we have a None
                pbar.update(1)
                for key in self.outputs():
                    results[key].append(None)
                continue

            user_includes = requested[1]["users"][0]

            results["text"].append(tweet.text)
            results["description"].append(user_includes.description)
            results["created_at"].append(tweet.created_at)
            results["name"].append(user_includes.name)
            results["screen_name"].append(user_includes.username)
            results["user_id"].append(user_includes.id)
            results["id"].append(user_includes.id)
            results["user_id_str"].append(str(user_includes.id))
            results["profile_image_url"].append(user_includes.profile_image_url.replace("_normal", ""))
            results["location"].append(user_includes.location)

        pbar.close()
        return results

def not_null(param):
    """
    k = pd.DataFrame({"text" : ["a", None, "b"]})

    @not_null("text")
    def method(data):
        return {"new_label" : [1 for _ in data.iterrows()]}

    print(class_.method(k)) # index at 1 should be None

    {'new_label': [1, None, 1]}

    """
    def Inner(func):
        def wrapper(*args, **kwargs):

            data = args[1]
            to_function = data[~(data[param].isna())]
            args = (args[0],) + (to_function,) + args[2:]
            resulted = func(*args, **kwargs)

            new_dict = dict()

            for keys in resulted:
                new_dict[keys] = [None] * len(data)
                for index, value in zip(to_function.index.values.tolist(), resulted[keys]):
                    new_dict[keys][index] = value

            return new_dict
        return wrapper
    return Inner

