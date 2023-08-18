class ChatInfo:

    def __init__(
            self,
            content: str,
            conversation_id: str,
            parent_id: str
    ):
        self.content = content
        self.conversation_id = conversation_id
        self.parent_id = parent_id
