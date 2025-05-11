import discord


class CharacterSelectButton(discord.ui.Button):
    def __init__(self, quest_manager, character, thread_name, user, message, embed):
        self.quest_manager = quest_manager
        self.character = character
        self.user = user
        self.message = message
        self.embed = embed
        super().__init__(label=thread_name, style=discord.ButtonStyle.primary, custom_id=str(character.profile_id))

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("This selection isn't for you.", ephemeral=True)
            return

        await interaction.response.defer()

        # Send message in thread with approval view
        thread = await self.character.get_character_thread()
        view = await JoinRequestView.create(self.quest_manager, thread.owner, self.character, self.message, self.embed)
        # embed = view.build_embed()

        details = ''

        character_thread = await self.character.get_character_thread()
        url = character_thread.jump_url

        character_tags = [
            tag.name
            for tag in character_thread.applied_tags
            if tag.name != 'Player Character'
        ]
        character_tag_text = f"{'/'.join(character_tags)}"

        character_text = f"as {url}. Level - {await self.character.level()} {character_tag_text}"
        details += f"{character_thread.owner.display_name} {character_text} joined the frey!\n"

        await interaction.channel.send(details, view=view)

        self.quest_manager.waitlisted_users.add(self.character)


class JoinRequestView(discord.ui.View):
    def __init__(self, quest_manager, thread_owner, character, message, embed):
        super().__init__(timeout=None)
        self.quest_manager = quest_manager
        self.thread_owner = thread_owner
        self.character = character
        self.message = message  # to store the message so we can edit it
        self.embed = embed

        self.add_item(ApproveButton(self, quest_manager))
        self.add_item(WaitlistButton(self, quest_manager))

    @classmethod
    async def create(cls, quest_manager, thread_owner, character, message, embed):
        self = cls(quest_manager, thread_owner, character, message, embed)

        self.quest_manager.waitlisted_users.add(self.character)
        await self.message.edit(embed=await self.build_embed())

        return self

    async def build_embed(self):
        async def user_list(adventurers):
            details = ''
            for adventurer in adventurers:
                character_thread = await adventurer.get_character_thread()
                url = character_thread.jump_url

                character_tags = [
                    tag.name
                    for tag in character_thread.applied_tags
                    if tag.name != 'Player Character'
                ]
                character_tag_text = f"{'/'.join(character_tags)}"
                character_text = f"as {url}. Level - {await adventurer.level()} {character_tag_text}"
                details += f"- {character_thread.owner.display_name} {character_text}\n"
            return details

        def update_or_add_field(name, value):
            for i, field in enumerate(self.embed.fields):
                if field.name == name:
                    self.embed.set_field_at(i, name=name, value=value, inline=False)
                    return
            self.embed.add_field(name=name, value=value, inline=False)

        for i, field in enumerate(self.embed.fields):
            if "interested in this quest" in field.name:
                total_adventurers = len(self.quest_manager.approved_users) + len(self.quest_manager.waitlisted_users)
                new_value = f"**{total_adventurers} player{'s are' if total_adventurers > 1 else ' is'} interested in this quest!**"

                self.embed.set_field_at(i, name=new_value, value=field.value, inline=False)

        update_or_add_field("✅ Approved", await user_list(self.quest_manager.approved_users))
        update_or_add_field("🕓 Waitlisted", await user_list(self.quest_manager.waitlisted_users))

        return self.embed

    async def update_message(self):
        if self.message:
            await self.message.edit(embed=await self.build_embed())


class ApproveButton(discord.ui.Button):
    def __init__(self, parent_view, quest_manager):
        super().__init__(label="Approve", style=discord.ButtonStyle.success)
        self.parent_view = parent_view
        self.quest_manager = quest_manager

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.parent_view.thread_owner:
            await interaction.response.send_message("Only the thread owner can approve players.", ephemeral=True)
            return

        user = self.parent_view.character
        if user not in self.quest_manager.approved_users:
            self.quest_manager.approved_users.add(user)
        if user in self.quest_manager.waitlisted_users:
            self.quest_manager.waitlisted_users.remove(user)

        await interaction.response.defer()
        await self.parent_view.update_message()


class WaitlistButton(discord.ui.Button):
    def __init__(self, parent_view, quest_manager):
        super().__init__(label="Waitlist", style=discord.ButtonStyle.secondary)
        self.parent_view = parent_view
        self.quest_manager = quest_manager

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.parent_view.thread_owner:
            await interaction.response.send_message("Only the thread owner can waitlist players.", ephemeral=True)
            return

        user = self.parent_view.character
        if user not in self.quest_manager.waitlisted_users:
            self.quest_manager.waitlisted_users.add(user)
        if user in self.quest_manager.approved_users:
            self.quest_manager.approved_users.remove(user)

        await interaction.response.defer()
        await self.parent_view.update_message()
