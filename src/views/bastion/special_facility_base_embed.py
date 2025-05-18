import discord


class SpecialFacilityBaseEmbed(discord.Embed):
    def __init__(self, facility, owner):
        title = facility.name
        description = facility.description
        color = discord.Color.blue()
        super().__init__(title=title, description=description, color=color)

    @classmethod
    async def create(cls, facility, owner):
        self = cls(facility, owner)
        char_thread = await owner.get_character_thread()

        starter_msg = await char_thread.fetch_message(char_thread.id)
        # If it has image attachments
        if starter_msg.attachments:
            for attachment in starter_msg.attachments:
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    image_url = attachment.url
                    break
            else:
                image_url = None
        else:
            image_url = None

        self.set_author(name=char_thread.name, url=char_thread.jump_url, icon_url=image_url)

        return self
