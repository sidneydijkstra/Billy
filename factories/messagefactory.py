import discord

from factories.embeddedfactory import EmbeddedFactory

class MessageFactory:
    # <-- error messages -->
    async def sendErrorMessage(context, command, error):
        await context.channel.send("Oops?!? Er gaat iets mis met het commando van %s!" % (context.author), embed=EmbeddedFactory.generateMessage(command, error))

    # <-- strategy messages -->
    async def sendStrategyAddMessage(channel, strategy):
        await channel.send("Ik heb het verzoekje van %s toegevoegd, B-B-Billy radio!!" % (strategy.author), embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyRemoveMessage(channel, strategy):
        await channel.send("", embed=EmbeddedFactory.generateMessage(("%s is verwijderd" % (strategy.title)), "%s heeft dit nummer uit de wachtrij gehaald! Klaag hem aan!" % (strategy.author)))

    async def sendStrategyPlayMessage(channel, strategy):
        await channel.send("B-B-B-Billy Radio met een verzoekje van %s!" % (strategy.author), embed=EmbeddedFactory.generateStrategyMessage(strategy))

    async def sendStrategyStopMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage("Ik heb de radio stop gezet!", "Je kan met !play een nieuw nummer in de wachtrij zetten."))

    async def sendStrategyQueueMessage(channel, queue):
        await channel.send("", embed=EmbeddedFactory.generateStrategyQueueMessage(queue))

    async def sendStrategyNoSkipMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage("Er zijn momenteel geen verzoekjes meer!", "Je kan met !play een nieuw nummer in de wachtrij zetten. Probeer het nu!"))

    async def sendStrategyNoSourceMessage(channel):
        await channel.send("", embed=EmbeddedFactory.generateMessage("Sorry maar ik kan je locale nummer niet vinden!", "Heb je het goed geschreven, spelling kan namelijk een lastig vak zijn!"))
