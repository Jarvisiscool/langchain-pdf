from pydantic import BaseModel
from langchain.schema import BaseChatMessageHistory

from app.web.api import (
    get_messages_by_conversation_id, 
    add_message_to_conversation
)

#SqlMessageHistory that makes use of conversation_id/chat_memory, SqlMessageHistory is a class that takes messages and stores them in a list. Responsible for persisting and retrieving messages. 
#get_messages_by_converation_id() gets messages tied to a conversation
#add_messages_by_conversation adds a single message
class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str
    
    @property
    def messages(self):
        return get_messages_by_conversation_id(self.conversation_id)
    
    def add_message(self, message):
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content 
        )
        
    def clear(self):
        pass