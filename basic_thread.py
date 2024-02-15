
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
                "author":message.author.display_name or None,
                "content": message.content or None,
                "created_at": message.created_at or None,
                "edited_at": message.edited_at or None,
                # "reactions": message.reactions
            })


