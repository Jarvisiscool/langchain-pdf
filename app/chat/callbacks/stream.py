from langchain.callbacks.base import BaseCallbackHandler

#Find out how to work the streaming for the website using StreamingHandler and a universal class called StreamableChain
#sends tokens to a queue whihc will then go to StreamableChain
class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
    #Sends in the chuncks of text
    def on_llm_new_token(self, token, **kwagrs):
        self.queue.put(token)
    
    #stops the loop and queue
    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)
    #if there is an error it will send None to stop the loop    
    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)
