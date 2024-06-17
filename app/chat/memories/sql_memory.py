#ConversationBufferMemory stores all messages of the conversation
from langchain.memory import ConversationBufferMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory

   
#creates a memory and puts it into the chat_history, input variable, and then get the output variables and store them: memory_key or output_key
def build_memory(chat_args):
    return ConversationBufferMemory(
        chat_memory=SqlMessageHistory(conversation_id=chat_args.conversation_id),
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )