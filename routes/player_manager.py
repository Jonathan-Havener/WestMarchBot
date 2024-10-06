from discord.ext import commands
from collections import OrderedDict


class PlayerManager(commands.Cog):
    def __init__(self, bot):
        print("PlayerManager cog initialized!")
        self.bot = bot
        self.information = [
            {
                "question": "What was the character's name?",
                "answer": ""
            },
            {
                "question": "What was the character's class?",
                "answer": ""
            },
            {
                "question": "What level was the character?",
                "answer": ""
            }
        ]

    @commands.command()
    async def ask_player_info(self, ctx, member_name):
        msg = f"Can you give me more information about {member_name}?"
        await ctx.channel.send(msg)
        for item in self.information:
            await ctx.send(item["question"])
            answer = await self.bot.wait_for('message')
            item["answer"] = answer.content

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.message_response_builder(message)

    async def handle_message_from_bot(self, message):
        ctx = await self.bot.get_context(message)

        if '!ask_player_info' in message.content:
            param = message.content.removeprefix("!ask_player_info")
            await self.ask_player_info(ctx, param)
        else:
            return

        await message.delete()

    async def message_response_builder(self, message):
        if message.author == self.bot.user:
            await self.handle_message_from_bot(message)