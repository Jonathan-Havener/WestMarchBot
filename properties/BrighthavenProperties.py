from pathlib import Path

GUILD_ID = 918112437331427358
QUEST_CHANNEL_ID = 1290373594781716554  # Replace with your category ID
bot_updates_channel_id = 1297996965438554142
ROLE_NAME = 'Adventurers of Brighthaven'
EXPIRY_FILE = 'bright_haven_role_expiry.json'
expiry_path = Path(__file__).parent.parent / "logs" / EXPIRY_FILE

# days
role_duration = 30
role_warning = 10