import discord
embedColor = 0xff0000

class EmbeddedFactory:
    # generate mention message
    def generateMentionMessage():
        embeddedBlock = discord.Embed(title="Verveling?", description="Als je niet weet wat je wil doen heb ik misschien wat voor je!", color=0x00ff00)
        embeddedBlock.add_field(name="Rustig Gamen", value="Hier heb ik een website waar je leuke games op kan spelen, veel plezier!\n<https://spele.nl/>", inline=False)
        embeddedBlock.add_field(name="Degelijk Wanken", value="Echt even snel een paar minuten voor jezelf, geniet ervan!\n<https://pornhub.com>", inline=False)
        embeddedBlock.add_field(name="Nieuwe Vlam", value="Opzoek naar een nieuwe liefde is altijd spannend, probeer het hier!\n<https://vijftigplusdating.nl>", inline=False)
        return embeddedBlock

    # generate embedded message
    def generateMessage(title, description):
        embeddedBlock = discord.Embed(title=title, description=description, color=embedColor)
        return embeddedBlock

    # generate strategy message
    def generateStrategyMessage(strategy):
        embeddedBlock = discord.Embed(title=strategy.getTitle(), description=strategy.getDescription(), color=embedColor)
        return embeddedBlock

    # generate strategy queue message
    def generateStrategyQueueMessage(queue):
        # check if queue is empty
        if len(queue) <= 0:
            return discord.Embed(title="Billy FM heeft niks af te spelen!", description="Doe !play om een nummer aan te vragen!", color=embedColor)
        # end if

        # generate embedded block
        embeddedBlock = discord.Embed(title="Nu op Billy FM!", description="Weet direct wat er te luisteren valt!", color=embedColor)
        # get size of queue
        size = len(queue) if len(queue) <= 5 else 5
        # loop max 5 entries in queue
        for i in range(size):
            # get strategy
            strategy = queue[i]
            # check if hidden then continue
            if strategy.hidden:
                continue
            # end if
            # add embedded field
            embeddedBlock.add_field(name=strategy.getTitle(), value=strategy.getDescription(), inline=False)
        # end for

        # check if queue was longer than max 5
        if len(queue) > 5:
            # add embedded field
            embeddedBlock.add_field(name=("[5/%d]" % (len(queue))), value="En nog meer...")
        # end if

        # return embed
        return embeddedBlock
