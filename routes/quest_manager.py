from discord.ext import commands


class QuestManager(commands.Cog):
    def __init__(self, bot):
        print("QuestManager cog initialized!")
        self.bot = bot
        self.managed_threads = {}

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        admin_user_id = 309102962234359829
        admin = self.bot.get_user(admin_user_id)
        if not admin:
            return
        message = await admin.send(f"The thread *{thread.name}* was created in *{thread.parent}*.\n"
                                   f"React :one: when this quest has completed.")
        self.managed_threads.update({message.id: thread})
        await message.add_reaction("1️⃣")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        if reaction.message.id in self.managed_threads.keys():
            thread = self.managed_threads[reaction.message.id]
            thread_members = await thread.fetch_members()
            member_names = [thread.guild.get_member(member.id).display_name for member in thread_members]
            msg = f"The thread participants are {member_names}"
            await reaction.message.channel.send(msg)

            for member in member_names:
                request_info_command = f"!ask_player_info {member}"
                await reaction.message.channel.send(request_info_command)