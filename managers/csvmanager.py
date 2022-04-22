import os
from datetime import datetime
from models.csvstorage import CSVStorage
from managers.configmanager import ConfigManager
FilesConfig = ConfigManager.get('files')

class CSVManager:
    # setup temp folder path
    csvFolderPath = FilesConfig['csvFolderPath']

    # create temp folder if not exists
    if not os.path.exists(csvFolderPath):
        os.makedirs(csvFolderPath)

    # create CSVStorage tables
    tables = {
        "configHistory": CSVStorage("{0}config_history.csv".format(csvFolderPath), [
            "id",
            "name",
            "path",
            "section",
            "oldValue",
            "newValue",
            "date"
        ]),
        "songHistory": CSVStorage("{0}song_history.csv".format(csvFolderPath), [
            "id",
            "name",
            "url",
            "requests"
        ])
    }

    # function for getting all keys in tables
    def keys():
        return CSVManager.tables.keys()

    # function to get table by key if exsist
    def get(name):
        if name in CSVManager.tables.keys():
            return CSVManager.tables[name]
        return None


    # function used to add new entrie in config_history.csv
    def addConfigHistory(id, name, path, section, oldValue, newValue):
        CSVManager.tables['configHistory'].table.add([id, name, path, section, oldValue, newValue, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
        CSVManager.tables['configHistory'].save()

    # function used to add new entrie in song_history.csv
    # this is not done by just adding the entrie but by first
    # checking if the enrtie already exsits and then either add
    # or update the entrie
    def addSongHistory(id, name, url):
        song = CSVManager.tables['songHistory'].table.find("id", id)
        print(song)
        if song:
            newRequests = str(int(song[3]) + 1)
            CSVManager.tables['songHistory'].table.update("id", id, [id, name, url, newRequests])
        else:
            CSVManager.tables['songHistory'].table.add([id, name, url, "1"])
        CSVManager.tables['songHistory'].save()
