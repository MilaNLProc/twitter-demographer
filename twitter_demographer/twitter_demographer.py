class Demographer:

    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def infer(self, data):
        for component in self.components:
            update = component.infer(data)
            for key, value in update.items():
                data[key] = value
            del component

        return data
