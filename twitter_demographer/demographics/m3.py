from twitter_demographer.components import Component
from m3inference import M3Inference
from m3inference import get_lang
import os
from twitter_demographer.support import utils
from multiprocessing import Pool
from appdirs import user_cache_dir
import shutil
import multiprocessing


class GenderAndAge(Component):
    """
    Provides a wrapper on the m3 dataset to predict age and binary gender in twitter data
    """

    def __init__(self):
        super().__init__()

    def outputs(self):
        return ["screen_name",
                "name",
                "user_id_str",
                "user_id",
                "id",
                "description",
                "profile_image_url"]

    def inputs(self):
        return ["user_id", "description", "profile_image_url", 'text']

    def infer(self, data):
        classifier = InternalGenderAgeFinder()

        results = self.initialize_return_dict()

        #data = data[list(results.keys())]

        to_test_data = data.drop_duplicates(subset=["screen_name"])

        to_test_data["lang"] = to_test_data["text"].apply(lambda x: get_lang(x))

        to_test_data = to_test_data.to_dict("records")

        cc = classifier.get_attribute_classification(to_test_data, batch_size=4)

        output_classifier = {
            "age": [],
            "gender": [],
            "is_org": []
        }

        for value in data["user_id"]:
            value = str(value)

            output_classifier["age"].append(cc[value]["age"])
            output_classifier["gender"].append(cc[value]["gender"])
            output_classifier["is_org"].append(cc[value]["is_org"])

        return output_classifier


class InternalGenderAgeFinder:

    def __init__(self):
        self.m3 = M3Inference()
        self.m3_noimg = M3Inference(use_full_model=False)

    def get_attribute_classification(self, users, batch_size):
        cache_dir = user_cache_dir("twitter_demographer", "images")

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        imaged_users = []
        without_image_users = []
        images = []

        for user in users:

            if ('user_id_str' in user) and (not ('user_id' in user)):
                user['user_id'] = str(user['user_id_str'])
            try:
                img_file_resize = "{}/{}_224x224.{}".format(cache_dir, user['user_id'],
                                                            utils.get_extension(user['profile_image_url']))
            except:
                img_file_resize = ""

            images.append((user['profile_image_url'], img_file_resize))
        cpus = multiprocessing.cpu_count() - 1 or 1
        with Pool(cpus) as p:
            outputs = p.starmap(utils.download_resize_img, images)

        for user, is_retrieved in zip(users, outputs):

            if ('user_id_str' in user) and (not ('user_id' in user)):
                user['user_id'] = str(user['user_id_str'])

            try:
                img_file_resize = "{}/{}_224x224.{}".format(cache_dir, user['user_id'],
                                                            utils.get_extension(user['profile_image_url']))
            except:
                img_file_resize = ""

            user['img_path'] = img_file_resize
            user['description'] = user['description']
            user['lang'] = user["lang"]

            if is_retrieved:
                imaged_users.append(user)
                print(imaged_users)
            else:
                without_image_users.append(user)

        pred_imaged = self.m3.infer(imaged_users, output_format='json', batch_size=batch_size)
        pred_without = self.m3_noimg.infer(without_image_users, output_format='json', batch_size=batch_size)
        fused = {**pred_imaged, **pred_without}

        shutil.rmtree(cache_dir)
        output_classifier = {}
        for key, value in fused.items():
            gender = 'male' if value['gender']["male"] > value['gender']["female"] else 'female'
            is_org = 'non-org' if value["org"]['non-org'] > value["org"]['is-org'] else 'is-org'
            age_dict = {k: v for (k, v) in value["age"].items()}
            age = max(age_dict, key=age_dict.get)

            output_classifier[str(key)] = {"age": age,
                                           "gender": gender,
                                           "is_org": is_org}

        return output_classifier
