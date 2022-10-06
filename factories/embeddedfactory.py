import discord
embedColor = 0xff0000

from managers.configmanager import ConfigManager
messagesConfig = ConfigManager.get('messages')

class EmbeddedFactory:
    # generate mention message
    def generateMentionMessage():
        embeddedBlock = discord.Embed(title=messagesConfig['mention']['title'], description=messagesConfig['mention']['description'], color=0x00ff00)
        for field in messagesConfig['mention']['fields']:
            embeddedBlock.add_field(name=field['title'], value=field['description'], inline=False)
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
    def generateStrategyQueueMessage(queue, page):
        
        print("real size: ", len(queue))
        
        pageSize = 5
        # remove all hidden strategies from queue
        queue = [strategy for strategy in queue if not strategy.hidden]
        popSize = page * pageSize
        
        print("filterd size: ", len(queue))
        
        if len(queue) <= 0 or len(queue) <= popSize:
            return discord.Embed(title=messagesConfig['strategyNoQueueMessage']['title'], description=messagesConfig['strategyNoQueueMessage']['description'], color=embedColor)
        # end if
        
        queue = queue[popSize:]
        
        # generate embedded block
        embeddedBlock = discord.Embed(title=messagesConfig['strategyQueueMessage']['title'], description=messagesConfig['strategyQueueMessage']['description'], color=embedColor)
        
        # get size of queue
        size = len(queue) if len(queue) <= 5 else pageSize
        print("print size: ", size)
        # loop max 5 entries in queue
        for i in range(size):
            # get strategy
            strategy = queue[i]
            
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
