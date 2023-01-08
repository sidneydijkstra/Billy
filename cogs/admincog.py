import io, sys, traceback
import discord
from discord.ext import commands

from clients.billycontroller import BillyController

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setstatus", help = "- Set custom status of bot.")
    @commands.is_owner()
    async def setStatus(self, ctx, args):
        if args:
            await BillyController.setStatus(args)

    
    @commands.command(name="setidle", help = "- Set bot status to idle.")
    @commands.is_owner()
    async def setIdle(self, ctx):
        await BillyController.setIdle()

    @commands.command(name="shutdown", aliases=["q", "quit"], help = "- Shutdown the bot.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        voice = ctx.voice_client
        if voice is not None:
            await voice.disconnect()
        await ctx.bot.close()

    @commands.command(name="python", aliases=["py"], help = "- Run python code.")
    @commands.is_owner()
    async def python(self, ctx):
        if not ctx.message == None and not ctx.message.reference == None:
            message = await ctx.fetch_message(ctx.message.reference.message_id)
            script = message.content.replace("```python", "").replace("```", "")

            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout

            result = "None"
            try:
                exec(script)
                result = sys.stdout.getvalue().strip()
            except SyntaxError as e:
                result = "Found error: %s\n\tAt line %d\n\tError details:\n\t- %s" % (e.__class__.__name__, e.lineno, e.args[0])
            except Exception as e:
                cl, exc, tb = sys.exc_info()
                result = "Found error: %s\n\tAt line %d\n\tError details:\n\t- %s" % (e.__class__.__name__, traceback.extract_tb(tb)[-1][1], e.args[0])
            finally: # !
                sys.stdout = old_stdout # !

            sys.stdout = old_stdout
            await message.channel.send("output:```" + result + "\n```")



def setup(bot):
    bot.add_cog(AdminCog(bot))
