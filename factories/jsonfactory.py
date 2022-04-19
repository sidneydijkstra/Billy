import json

class JsonFactory:
    def load(path):
        with open(path) as file:
            return json.load(file)


    def save(path, object):
        with open(path, 'w') as file:
            json.dump(object, file)
