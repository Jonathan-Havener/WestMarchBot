from discord.ext import commands


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(guild_messages=True)
    async def ping(self, ctx):
        await ctx.send('Pong!')
