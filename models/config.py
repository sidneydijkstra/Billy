from models.jsonstorage import JsonStorage

class Config:
    config = JsonStorage("./assets/config/config.json")

    def get():
        return Config.config

    def section(section):
        return Config.config.object[section]
