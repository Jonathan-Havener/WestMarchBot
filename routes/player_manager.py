from discord.ext import commands
from collections import OrderedDict


class PlayerManager(commands.Cog):
    def __init__(self, bot):
        print("PlayerManager cog initialized!")
        self.bot = bot
        self.message_chain = OrderedDict()
        self.message_chain["What was the character's name?"] = None
        self.message_chain["What was the character's class?"] = None
        self.message_chain["What level was the character?"] = None

    @commands.command()
    async def ask_player_info(self, ctx, member_name):
        msg = f"Can you give me more information about {member_name}?"
        await ctx.channel.send(msg)
        await self.send_next_message_in_chain(ctx.message)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.message_response_builder(message)

    async def send_next_message_in_chain(self, message):
        question = None
        for key, value in self.message_chain.items():
            if not value:
                question = key
                break
        if question:
            await message.channel.send(question)
        else:
            congrats= f"Heres the information! {self.message_chain}"
            await message.channel.send(congrats)

    async def handle_message_response_chain(self, message):
        question = message.reference.cached_message.content
        self.message_chain[question] = message.content
        await self.send_next_message_in_chain(message)

    async def handle_message_from_bot(self, message):
        ctx = await self.bot.get_context(message)

        if '!ask_player_info' in message.content:
            param = message.content.removeprefix("!ask_player_info")
            await self.ask_player_info(ctx, param)
        else:
            return

        await message.delete()

    async def message_response_builder(self, message):
        if (message.reference
                and message.reference.cached_message
                and message.reference.cached_message.author == self.bot.user):
            await self.handle_message_response_chain(message)

        if message.author == self.bot.user:
            await self.handle_message_from_bot(message)