import os
import redis

#Easier to work with
client = redis.Redis.from_url(
    os.environ["REDIS_URI"],
    #Redis gives bytes, decodes it into to strings; easier to read
    decode_responses=True
)
