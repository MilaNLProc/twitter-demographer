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
            self.local_inputs.extend(component.outputs() + component.inputs()) # first run we add both
        else:
            if set(component.inputs()) <= set(self.local_inputs):
                self.components.append(component)
            else:
                raise Exception("Some of the fields are not supported by this composition")

    def infer(self, data):

        for component in self.components:
            update = component.infer(data)
            for key, value in update.items():
                data[key] = value

            if self.cache_steps:
                data.to_parquet("local.csv", engine="pyarrow")
            del component

        return data
