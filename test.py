from langchain_community.chat_models import ChatOpenAI 
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()

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


chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{content}")
    ]
)

#Overrides the chain's stream method
#stream method returns generator that produces strings that are readable
#Allows from stream method to run within a chain because chains do not like streaming
#Mixin that can be used anywhere
class StreamableChain:
    def stream(self, input):
        #creates queue's for different users/requests
        queue = Queue()
        #creates handler for different users/requests gets queue and assigns it to a variable
        handler = StreamingHandler(queue)
        
        #Allows for everytime the chain is run there will be a callback to StreamingHandler
        def task():
            self(input, callbacks=[handler])
        #Allows it to run concurrently with the chain so it will look like it is streaming
        Thread(target=task).start()
        #Checks to see whether there are any texts streaming into the queue
        #Stops the while loop from checking when None is passed
        while True:
            token= queue.get()
            if token is None:
                break
            yield token

#Allows for streaming support for many different kinds of chains such as ConversationalChain, LLMChain or any other chain
#Create a new class like the one below and add whatever you want to extend next to StreamabelChain
class StreamingChain(StreamableChain, LLMChain):
    pass

#streaming from a chain
chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content":"tell me a joke"}):
    print(output)