from transformers import AutoTokenizer, AutoConfig
from twitter_demographer.support.m3supporter import GenderAgeFinder
from tqdm import tqdm
import tweepy

class Component:

    def __init__(self):
        pass

    def infer(self, *args):
        pass

class Rehydrate(Component):

    def __init__(self, bearer_token, fields_of_interest):
        super().__init__()
        self.api = tweepy.Client(bearer_token, wait_on_rate_limit=True)
        self.fields_of_interest = fields_of_interest

    def infer(self, data):
        results = {
            "screen_name": [],
            "name": [],
            "user_id_str": [],
            "user_id": [],
            "id": [],
            "profile_image_url": [],
            "description": [],
            "created_at": [],
            "text": []
        }
        pbar = tqdm(total=len(data))
        for tweet_id in data["tweet_ids"]:
            call = self.api.get_tweet(tweet_id, tweet_fields=[
                                            'id', 'text', 'author_id', 'created_at', 'conversation_id',
                                            'entities',
                                            'public_metrics', 'referenced_tweets'
                                        ],
                                      expansions=[
                                            'author_id', 'referenced_tweets.id', 'referenced_tweets.id.author_id',
                                        ],
                                      place_fields=['full_name', 'id'],
                                      user_fields=[
                                            'id', 'name', 'username', 'profile_image_url', 'description'
                                        ])
            pbar.update(1)
            tweet = call[0]
            user_includes = call[1]["users"][0]

            results["text"].append(tweet.text)
            results["description"].append(user_includes.description)
            results["created_at"].append(tweet.created_at)
            results["name"].append(user_includes.name)
            results["screen_name"].append(user_includes.username)
            results["user_id"].append(user_includes.id)
            results["id"].append(user_includes.id)
            results["user_id_str"].append(str(user_includes.id))
            results["profile_image_url"].append(user_includes.profile_image_url.replace("_normal", ""))

        pbar.close()
        return results


class M3GenderAndAge:

    def __init__(self):
        pass

    def infer(self, data):
        classifier = GenderAgeFinder()

        results = {
            "screen_name": [],
            "name": [],
            "user_id_str": [],
            "user_id": [],
            "id": [],
            "description" : [],
            "profile_image_url": [],
        }


        data = data[list(results.keys())]
        to_test_data = data.drop_duplicates(subset=["screen_name"])

        to_test_data = to_test_data.to_dict("records")
        print(to_test_data)
        cc = classifier.get_attribute_classification(to_test_data, batch_size=4)

        output_classifier = {
            "age" : [],
            "gender": [],
            "is_org": []
        }
        for value in data["user_id"]:
            value = str(value)

            output_classifier["age"].append(cc[value]["age"])
            output_classifier["gender"].append(cc[value]["gender"])
            output_classifier["is_org"].append(cc[value]["is_org"])

        return output_classifier


class HuggingFaceClassifier:

    def __init__(self, model_name):
        self.model_name = model_name

    def load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        config = AutoConfig.from_pretrained(self.model_name)



