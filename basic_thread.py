import re
import logging


class Basic_Thread():
    def __init__(self, thread_obj, message_list):

        self.archive_timestamp = thread_obj.archive_timestamp or None
        self.created_at = thread_obj.created_at or None
        self.id = thread_obj.id or None
        self.member_count = thread_obj.member_count or None
        self.message_count = thread_obj.message_count or None
        self.name = thread_obj.name or None
        self.owner = thread_obj.owner.display_name if thread_obj.owner else None
        self.messages = []
        for message in message_list:
            self.messages.append({
                "author": message.author.display_name or None,
                "content": message.content or None,
                "created_at": message.created_at or None,
                "edited_at": message.edited_at or None,
            })

        self.logger = logging.getLogger(self.name)
        self.build_logger()

    def build_logger(self):
        # Create a formatter with your desired format
        formatter = logging.Formatter(f'%(levelname)s - Thread:\t{self.name} \n '
                                      f'\t\tOwner:\t{self.owner} \n'
                                      f'\t\t%(message)s')
        # Create a handler for writing log messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set the handler level to DEBUG
        console_handler.setFormatter(formatter)
        # Add the console handler to the logger
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)

    @property
    def members(self):
        return set([msg["author"] for msg in self.messages])

    @property
    def messages_by_author(self):
        msg_by_author = {}
        for author in self.members:
            msg_by_author[author] = []
        for message in self.messages:
            author = message["author"]
            msg_by_author[author].append(message)
        return msg_by_author

    @property
    def member_levels(self):
        author_levels = {}
        msgs_by_author = self.messages_by_author
        for author_msgs in msgs_by_author:
            author = msgs_by_author[author_msgs][0]["author"]
            if author == self.owner:
                # The creator of a thread won't have a character level
                continue
            level = self.get_player_level_from_msg_list(msgs_by_author[author_msgs])
            author_levels.update({author: level})
        return author_levels

    def get_player_level_from_msg_list(self, msg_list):
        level_pattern = r"le?ve?l ?(?P<level>\d)"
        level = None
        for msg in msg_list:
            if not msg["content"]:
                continue
            res = re.findall(level_pattern, msg["content"], re.IGNORECASE)
            if res:
                res = [int(num) for num in res]
                level = sum(res)
                break

        if level is None:
            self.logger.debug(f"Could not find level for {msg_list[0]['author']} from {[msg['content'] for msg in msg_list]}")
        return level

from collections import OrderedDict
def get_player_histories(thread_history):
    player_history = {}
    for thread in thread_history:
        mem_levels = thread_history[thread].member_levels
        for player in mem_levels:
            hist_obj = {
                thread_history[thread].created_at: {
                    "level": mem_levels[player],
                    "thread": thread
                }
            }
            if player not in player_history:
                player_history[player] = hist_obj
            player_history[player].update(hist_obj)

    player_history = OrderedDict(sorted(player_history.items()))
    for player in player_history:
        player_history[player] = OrderedDict(sorted(player_history[player].items()))
    return player_history