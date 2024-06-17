from langchain.memory import ConversationBufferWindowMemory
from app.chat.memories.histories.sql_history import SqlMessageHistory

def window_buffer_window_memory(chat_args):
    return ConversationBufferWindowMemory(
        memory_key = "chat_history",
        output_key = "answer",
        return_messages = True,
        #Same as ConversationBufferMemory expcept that the k allows you to regulate the amount of exchanges you need to extract from SqlMessageHistory
        chat_memory = SqlMessageHistory(
            conversation_id = chat_args.conversation_id
        ),
        k=2
    )