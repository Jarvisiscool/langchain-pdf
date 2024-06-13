from .chatopenai import build_llm
from functools import partial
llm_map = {"gpt-4": partial(build_llm, model_name="gpt-4"), "gpt-3.5-turbo": build_llm}


builder = llm_map["gpt-4"]
builder(chat_args)