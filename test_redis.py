import redis

# Connect to Redis
redis_instance = redis.StrictRedis(host="localhost", port=6379, db=0)

def store_access_token(user_id, access_token):
    # Store the access token in Redis with an expiration time
    redis_instance.set(user_id, str(access_token), ex=120)

def fetch_access_token(user_id):
    # Fetch the access token from Redis
    access_token = redis_instance.get(user_id)
    if access_token:
        return access_token.decode()  # Decode bytes to string
    else:
        return None

store_access_token("12345", "sgdyuadiasd")

token = fetch_access_token("12345")

print(token)
