from langchain.chat_models import ChatOpenAI

#Instance of ChatOpenAI that has streaming and name of the model you want to use
def build_llm(chat_args, model_name):
    return ChatOpenAI(streaming=chat_args.streaming, model_name=model_name)