from models.jsonstorage import JsonStorage

class Config:
    config = JsonStorage("./assets/config/config.json")
    messages = JsonStorage("./assets/config/messages.json")

    def get(section = ''):
        if section == '':
            return Config.config
        else:
            return Config.config.object[section]

    def section(section):
        return Config.config.object[section]
