import abc
import numpy as np
import pandas as pd
import random
from tqdm import tqdm
import tweepy
from tweepy.errors import BadRequest
import transformers
from abc import ABC
from twitter_demographer.support.utils import chunks

transformers.logging.set_verbosity(transformers.logging.ERROR)

class Component(ABC):
    """
    Abstract component class
    """

    def __init__(self, **kwargs):
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


        tweet_ids = data["tweet_ids"].values.tolist()
        pbar = tqdm(total=len(data), position=1)

        good_tweets = {}

        for split in chunks(tweet_ids, 99):
            split = ",".join(list(map(str,split)))

            requested = self.api.get_tweets(split,
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

            user_mapping_dict = {k["id"]: k for k in requested[1]["users"]}
            tweets = requested[0]

            for tweet in tweets:
                results = {}

                pbar.set_description("Running Hydrate")
                user_id = tweet["author_id"]

                user_includes = user_mapping_dict[user_id]
                results["text"] = tweet.text
                results["description"] = user_includes.description
                results["created_at"] = tweet.created_at
                results["name"] = user_includes.name
                results["screen_name"] = user_includes.username
                results["user_id"] = user_includes.id
                results["id"] = user_includes.id
                results["user_id_str"] = str(user_includes.id)
                results["profile_image_url"] = user_includes.profile_image_url.replace("_normal", "")
                results["location"] = user_includes.location
                good_tweets[tweet.id] = results

            # we know get all the tweets that we were not able to reconstruct
            errors = requested[2]
            for error in errors:
                pbar.update(1)
                results = {}

                for field in self.outputs():
                    results[field] = (None)

                good_tweets[int(error["value"])] = results

            pbar.update(99)
        pbar.close()

        results = self.initialize_return_dict()
        for tw_id in data["tweet_ids"].values.tolist():
            for field in self.outputs():
                results[field].append(good_tweets[int(tw_id)][field])

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

def repropagate_on_duplicates(param):
    """
    k = pd.DataFrame({"text" : ["a", None, "b"]})


    """
    raise Exception("Not Implemented")
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

def label_swapper(dataframe, percentage=0.01):
    msk = np.random.rand(len(dataframe)) < percentage
    shuffle = dataframe[msk]
    rest = dataframe[~msk]

    col = random.choice(shuffle.cloumns)

    vals = shuffle[col].values.tolist()
    random.shuffle(vals)
    shuffle[col] = vals

    dataframe = pd.concat([rest, shuffle]).sample(frac=1)

    return dataframe


