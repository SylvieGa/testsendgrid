import os
import smartninja_redis
import uuid

redis = smartninja_redis.from_url(os.environ.get("REDIS_URL"))

def create_csrf_token(username):
    csrf_token = str(uuid.uuid4())

    print("CSRF-Token: "+csrf_token)

    redis.set(name=csrf_token, value=username)

    return csrf_token

def validate_csrf(csrf, username):
    redis_csrf_username = redis.get(name=csrf)

    if redis_csrf_username:
        csrf_username = redis_csrf_username.decode()

        print("CSRF: " + str(csrf_username))

        return username == csrf_username
    else:
        return False