from pathlib import Path

GUILD_ID = 918112437331427358
QUEST_CHANNEL_ID = 1064019917579497592  # Replace with your category ID
bot_updates_channel_id = 1292599936474681384
ROLE_NAME = 'Adventurers of New Devlin'
EXPIRY_FILE = 'new_devlin_role_expiry.json'
expiry_path = Path(__file__).parent.parent / "logs" / EXPIRY_FILE

# days
role_duration = 90
role_warning = 20