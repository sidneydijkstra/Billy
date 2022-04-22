from factories.csvfactory import CSVFactory

class CSVStorage():
    def __init__(self, path, headers):
        self.path = path
        self.table = CSVFactory.create(path, headers)

    def save(self):
        CSVFactory.save(self.path, self.table)

    # util
    def show(self):
        print(self.table)
