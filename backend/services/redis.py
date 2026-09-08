import redis as redis


class RedisManager:

    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True,
            password = None,
        )
    

    def set_something(self):
        self.client.set("hii" , "hello")
    
    def get_something(self):
        return self.client.get("hii")
    
redisclient = RedisManager()