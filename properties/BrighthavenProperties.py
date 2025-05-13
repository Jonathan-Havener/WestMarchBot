from pathlib import Path
import os
from dotenv import load_dotenv

GUILD_ID = int(os.environ.get("SERVER_ID"))
QUEST_CHANNEL_ID = int(os.environ.get("QUEST_BOARD_ID"))  # Replace with your category ID
bot_updates_channel_id = int(os.environ.get("BOT_UPDATES_ID"))
ROLE_NAME = 'Adventurers of Brighthaven'
EXPIRY_FILE = 'bright_haven_role_expiry.json'
expiry_path = Path(__file__).parent.parent / "logs" / EXPIRY_FILE

# days
role_duration = 30
role_warning = 10