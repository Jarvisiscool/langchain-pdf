from .sql_memory import build_memory
#Allows you to disregard info that is not related to question asked and only takes memory that is relevant
from .window_memory import window_buffer_window_memory

#Dictionary that holds keys for type of memory
memory_map = {
    "sql_buffer_memory": build_memory,
    "sql_window_memory": window_buffer_window_memory
}