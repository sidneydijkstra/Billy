from factories.jsonfactory import JsonFactory

class JsonStorage():
    def __init__(self, path):
        self.path = path
        self.object = JsonFactory.load(path)

    def save(self):
        JsonFactory.save(self.path, self.object)

    # util
    def show(self):
        print(self.object)
