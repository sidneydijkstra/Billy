import discord

from factories.embeddedfactory import EmbeddedFactory
from managers.configmanager import ConfigManager
messagesConfig = ConfigManager.get('messages')

class MessageFactory:
    # <-- error messages -->
    async def sendErrorMessage(context, command, error):
        await context.channel.send(messagesConfig['errorMessage'] % (context.author), embed=EmbeddedFactory.generateMessage(command, error))

    # <-- config messages -->
    async def sendConfigError(channel, path, error):
        await channel.send((messagesConfig['configError'] % ('/'.join(path))) + ("\n```\n%s\n```" % (error)))

    async def sendConfigEdit(channel, path, value):
        await channel.send((messagesConfig['configEdit'] % ('/'.join(path))) + ("\n```\n%s\n```" % (value)))

    async def sendConfigShow(channel, path, value):
        await channel.send((messagesConfig['configShow'] % ('/'.join(path))) + ("\n```\n%s\n```" % (value)))

    async def sendConfigList(channel, value):
        await channel.send(messagesConfig['configList'] + ("\n```\n%s\n```" % (value)))

    # <-- stats messages -->
    async def sendStatsError(channel, error):
        await channel.send(messagesConfig['statsError'] + ("\n```\n%s\n```" % (error)))

    async def sendStatsList(channel, value):
        await channel.send(messagesConfig['statsList'] + ("\n```\n%s\n```" % (value)))

    async def sendStatsShow(channel, name, table):
        tableContent = ""
        for row in table:
            tableContent += ', '.join(row) + "\n"
        await channel.send(messagesConfig['statsShow'] % (name) + ("\n```\n%s\n```" % (tableContent)))

    async def sendStatsTopSongs(channel, table, size):
        tableContent = ""
        for i, row in enumerate(table):
            number = "**%s.**" % str(i+1)
            content = row[1]
            amount = " *[%s]*" % row[3]
            array = [number, content, amount]
            tableContent += ' '.join(array) + "\n"
        await channel.send(messagesConfig['statsTopSongs'] % (str(size)) + ("\n\n%s\n" % (tableContent)))

    # <-- strategy messages -->
    async def sendStrategyAddMessage(channel, strategy):
        await channel.send(messagesConfig['strategyAddMessage'] % (strategy.author), embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyRemoveMessage(channel, strategy):
        await channel.send("", embed=EmbeddedFactory.generateMessage((messagesConfig['strategyRemoveMessage']['title'] % (strategy.title)), messagesConfig['strategyRemoveMessage']['description'] % (strategy.author)))

    async def sendStrategyPlayMessage(channel, strategy):
        await channel.send(messagesConfig['strategyPlayMessage'] % (strategy.author), embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyNowMessage(channel, strategy):
        await channel.send(messagesConfig['strategyNowMessage'], embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyStopMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage(messagesConfig['strategyStopMessage']['title'], messagesConfig['strategyStopMessage']['description']))

    async def sendStrategyQueueMessage(channel, queue, page):
        await channel.send("", embed=EmbeddedFactory.generateStrategyQueueMessage(queue, page))

    async def sendStrategyNoSkipMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage(messagesConfig['strategyNoSkipMessage']['title'], messagesConfig['strategyNoSkipMessage']['description']))

    async def sendStrategyNoSourceMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage(messagesConfig['strategyNoSourceMessage']['title'], messagesConfig['strategyNoSourceMessage']['description']))
