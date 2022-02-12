import discord

class EmbeddedFactory:
    def generateMentionMessage():
        embeddedBlock = discord.Embed(title="Verveling?", description="Als je niet weet wat je wil doen heb ik misschien wat voor je!", color=0x00ff00)
        embeddedBlock.add_field(name="Rustig Gamen", value="Hier heb ik een website waar je leuke games op kan spelen, veel plezier!\n<https://spele.nl/>", inline=False)
        embeddedBlock.add_field(name="Degelijk Wanken", value="Echt even snel een paar minuten voor jezelf, geniet ervan!\n<https://pornhub.com>", inline=False)
        embeddedBlock.add_field(name="Nieuwe Vlam", value="Opzoek naar een nieuwe liefde is altijd spannend, probeer het hier!\n<https://vijftigplusdating.nl>", inline=False)
        return embeddedBlock

    def generateAudioInfoMessage(audioInfo):
        embeddedBlock = discord.Embed(title=("%s [%s]" % (audioInfo.title, audioInfo.duration)), description=("%d Views - By %s - id: %d" % (audioInfo.views, audioInfo.uploader, audioInfo.id)), color=0xff0000)
        return embeddedBlock

    def generateAudioRemoveMessage(audioInfo):
        embeddedBlock = discord.Embed(title=("%s is verwijderd" % (audioInfo.title)), description=("%s heeft dit nummer uit de wachtrij gehaald! Klaag hem aan!" % (audioInfo.auther)), color=0xff0000)
        return embeddedBlock

    def generateAudioQueueMessage(queue):
        embeddedBlock = discord.Embed(title="Nu op Billy FM!", description="Weet direct wat er te luisteren valt!", color=0xff0000)
        size = len(queue) if len(queue) <= 5 else 5
        for i in range(size):
            audioInfo = queue[i]
            embeddedBlock.add_field(name=("%d: %s [%s]" % (i+1, audioInfo.title, audioInfo.duration)), value=("%d Views - By %s - id: %d" % (audioInfo.views, audioInfo.uploader, audioInfo.id)), inline=False)

        if len(queue) > 5:
            embeddedBlock.add_field(name=("[5/%d]" % (len(queue))), value="En nog meer...")

        return embeddedBlock

    def generateAudioQueueEmptyMessage():
        embeddedBlock = discord.Embed(title="Billy FM heeft niks af te spelen!", description="Doe !play om een nummer aan te vragen!", color=0xff0000)
        return embeddedBlock
