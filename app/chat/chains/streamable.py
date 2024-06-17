from flask import current_app
from queue import Queue
from threading import Thread
from app.chat.callbacks.stream import StreamingHandler

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