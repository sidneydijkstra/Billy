import discord

from models.config import Config
messages = Config.messages.object
from factories.embeddedfactory import EmbeddedFactory


class MessageFactory:
    # <-- error messages -->
    async def sendErrorMessage(context, command, error):
        await context.channel.send(messages['errorMessage'] % (context.author), embed=EmbeddedFactory.generateMessage(command, error))

    # <-- strategy messages -->
    async def sendStrategyAddMessage(channel, strategy):
        await channel.send(messages['strategyAddMessage'] % (strategy.author), embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyRemoveMessage(channel, strategy):
        await channel.send("", embed=EmbeddedFactory.generateMessage((messages['strategyRemoveMessage']['title'] % (strategy.title)), messages['strategyRemoveMessage']['description'] % (strategy.author)))

    async def sendStrategyPlayMessage(channel, strategy):
        await channel.send(messages['strategyPlayMessage'] % (strategy.author), embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyStopMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage(messages['strategyStopMessage']['title'], messages['strategyStopMessage']['description']))

    async def sendStrategyQueueMessage(channel, queue):
        await channel.send("", embed=EmbeddedFactory.generateStrategyQueueMessage(queue))

    async def sendStrategyNoSkipMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage(messages['strategyNoSkipMessage']['title'], messages['strategyNoSkipMessage']['description']))

    async def sendStrategyNoSourceMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage(messages['strategyNoSourceMessage']['title'], messages['strategyNoSourceMessage']['description']))
