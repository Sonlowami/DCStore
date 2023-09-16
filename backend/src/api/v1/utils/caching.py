import redis
from dotenv import load_dotenv
from api.v1.utils.config import Config

load_dotenv()

redis_client = redis.StrictRedis.from_url(Config.REDIS_URI)
