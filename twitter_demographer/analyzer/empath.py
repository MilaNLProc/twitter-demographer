from empath import Empath
from twitter_demographer.components import Component


class EmpathAnalyzer(Component):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outputs(self):
        return [f"empath_{k}" for k in Empath().analyze("test").keys()]

    def inputs(self):
        return ["text"]

    def infer(self, data):
        lexicon = Empath()
        results = self.initialize_return_dict()

        for tweet in data["text"].values.tolist():
            counts = lexicon.analyze(tweet, normalize=True)

            for item, value in counts.items():
                results[f"empath_{item}"].append(value)

        return results
