import os
import redis

#Easier to work with
client = redis.Redis.from_url(
    os.environ["REDIS_URI"],
    decode_responses=True
)
