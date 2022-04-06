from twitter_demographer.components import Component, not_null
import re
import liwc
from collections import Counter

def liwc_tokenize(text):
    text = text.lower()
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

class LIWCAnalyzer(Component):
    """
    A wrapper over LIWC files
    """

    def __init__(self, liwc_dic, **kwargs):
        """

        :param liwc_dic: this is the liwc file. The method exepcts something like "LIWC2007_English100131.dic"
        :param kwargs:
        """

        parse, category_names = liwc.load_token_parser(liwc_dic)
        self.category_names = category_names
        self.parse = parse
        super().__init__(**kwargs)

    def outputs(self):
        return [f"LIWC_{k}" for k in self.category_names]

    def inputs(self):
        return ["text"]

    @not_null("text")
    def infer(self, data, *args):

        results = self.initialize_return_dict()

        for text in data["text"].values.tolist():
            tokens = liwc_tokenize(text)

            counts = dict(Counter(category for token in tokens for category in self.parse(token)))

            for item, value in counts.items():
                results[f"LIWC_{item}"].append(value)

        return results

