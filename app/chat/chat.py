import random
from app.chat.score import random_component_by_score
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llm import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import (set_conversation_components, get_conversation_components)


def select_component(component_type, component_map, chat_args):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]
    
    if previous_component:
        #NOT first message need to use the same retriever
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        #first message; need to pick a random retriever
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)
    
#define a function, use retriever, customize retriever, then creates a custom memory
#ConversationBufferMemory stores the data in a plain list, modifies the input and output variables
#ConversationSummaryMemory which summarized the data and outputs the summary
#creates retriever, memory, and llm, which will then use StreamingConversationalRetrievalChain to retrieve the needed text output the answer using the llm and store the answer in a SqlMemory  
#Builds and returns the StreamingConversationalRetrievalChain, it supports streaming, and creates random variations of retriever, memory, and llm model
def build_chat(chat_args: ChatArgs):
    retriever_name, retriever = select_component(
        "retriever",
        retriever_map,
        chat_args
    )
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)
    
    set_conversation_components(chat_args.conversation_id, llm=llm_name, retriever= retriever_name, memory= memory_name)

    condense_question_llm = ChatOpenAI(streaming=False)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata = chat_args.metadata
    )
