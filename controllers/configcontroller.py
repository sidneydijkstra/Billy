import random

from factories.messagefactory import MessageFactory
from clients.billycontroller import BillyController
from managers.configmanager import ConfigManager
from managers.csvmanager import CSVManager

class ConfigController:
    def __init__(self):
        pass

    async def edit(self, author, path, content):
        # try to get config section from path
        _, _, oldValue = self.getConfigSection(path)
        # try to set path section to content
        state, name, value = self.setConfigSection(path, content)
        # check if state is true
        if state:
            # save changes to config
            ConfigManager.save()
            # make history entrie
            CSVManager.addConfigHistory(author.id, author.name, '/'.join(path), name, oldValue, value)
            # send edit message
            await MessageFactory.sendConfigEdit(BillyController.getChannel(), path, self.stringConfig(name, value))
        # end if

        # if state is false
        else:
            # send error message
            await MessageFactory.sendConfigError(BillyController.getChannel(), path, value)
        # end else

    async def show(self, author, path):
        # try to get path section
        state, name, value = self.getConfigSection(path)
        # check if state is true
        if state:
            # send show message
            await MessageFactory.sendConfigShow(BillyController.getChannel(), path, self.stringConfig(name, value))
        # end if

        # if state is false
        else:
            # send error message
            await MessageFactory.sendConfigError(BillyController.getChannel(), path, value)
        # end else

    async def list(self, author):
        # send list message
        await MessageFactory.sendConfigList(BillyController.getChannel(), self.stringConfig("Config", ConfigManager.get()))

    # function to get a config section if exists
    # return variables are (state, name, value)
    # on result True (True, "Key", "Value")
    # on result False (False, "Key", "Error")
    def getConfigSection(self, path):
        name = ""
        value = ConfigManager.get()
        for index in path:
            if index in value:
                name = index
                value = value[index]
            else:
                return False, index, "{0} not in dict".format(index)
        return True, name, value

    # function to set a config section if exists
    # return variables are (state, name, value)
    # on result True (True, "Key", "Value")
    # on result False (False, "Key", "Error")
    def setConfigSection(self, path, content):
        name = ""
        value = ConfigManager.get()
        section = None
        for index in path:
            if index in value:
                name = index
                section = value
                value = value[index]
            else:
                return False, index, "{0} not in dict".format(index)

        if isinstance(value, dict) or isinstance(value, list):
            return False, index, "{0} not editable value".format(index)

        section[name] = content

        return True, name, content

    # function for creating message from config section name and Value
    # this function returns a string used in a code block
    def stringConfig(self, name, value):
        message = "{0}: ".format(name)
        if isinstance(value, dict):
            message = message + "\n"
            for key in value:
                message = message + " - {0}\n".format(key)
        elif isinstance(value, list):
            message = message + "[\n"
            for item in value:
                message = message + " {0}\n".format(key)
            message = message + "]\n"
        else:
            message = message + str(value)
        return message
