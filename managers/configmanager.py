from models.jsonstorage import JsonStorage

class ConfigManager:
    config = JsonStorage("./assets/config/config.json")

    def get(section = ''):
        if section == '':
            return ConfigManager.config.object
        else:
            return ConfigManager.config.object[section]

    def save():
        ConfigManager.config.save()
