import io, sys, traceback, copy
import discord
from discord.ext import commands

from clients.billycontroller import BillyController
from managers.csvmanager import CSVManager
from factories.messagefactory import MessageFactory

class StatsCog(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.command(name="stats")
    async def stats(self, ctx, *args):
        # create empty table variable
        table = None

        # chech if list command
        if len(args) > 0 and "-l" in args[0]:
            # send stats list message
            await MessageFactory.sendStatsList(BillyController.getChannel(), '\n'.join(CSVManager.keys()))
        #end if

        # check if len of args is greater then 0
        elif len(args) > 0:
            # get csv table
            csvTable = CSVManager.get(args[0])
            # check if csvTable not None
            if not csvTable:
                # send stats error message
                await MessageFactory.sendStatsError(BillyController.getChannel(), "{0} is None".format(args[0]))
                # return from function
                return
            # end if

            # check if get limit command (!stats name limit) (!stats statpanel 5)
            if len(args) == 2 and args[1].isdigit():
                # set table variable
                table = csvTable.table.get(int(args[1]))
            # end if
            # check if get limit direction command (!stats name limit direction) (!stats statpanel 5 False)
            elif len(args) > 2 and args[1].isdigit() and ("True" in args[2] or "False" in args[2]):
                # set table variable
                table = csvTable.table.get(int(args[1]), ("True" in args[2]))
            # end elif
            # check if pick command (!stats name start end) (!stats statpanel 1 5)
            elif len(args) > 2 and args[1].isdigit() and args[2].isdigit():
                # set table variable
                table = csvTable.table.pick(int(args[1]), int(args[2]))
                # if table is None
                if table == None:
                    # send stats error message
                    await MessageFactory.sendStatsError(BillyController.getChannel(), "[{0}:{1}] are None".format(args[1],args[2]))
                # end if
            # end elif
            # on normal get command (!stats name) (!stats statpanel)
            else:
                # set table variable
                table = csvTable.table.all()
            # end else
        # end elif

        # if table variable not None
        if not table == None:
            # insert header into start of array
            table = copy.copy(table)
            table.insert(0, csvTable.table.headers())
            # send stats show message
            await MessageFactory.sendStatsShow(BillyController.getChannel(), args[0], table)
        # end if

def setup(bot):
    bot.add_cog(StatsCog(bot))
