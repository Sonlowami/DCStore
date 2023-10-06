from datetime import datetime
import json

from api.v1.utils.caching import redis_client

class RecentFiles:
    MAX_STACK = 5

    @staticmethod
    def add_file_to_recent_files(user_id, file_id, info):
        """Add file to recent files"""
        info["datetime"] = datetime.now().isoformat()
        key = f"recent_files:{user_id}"
        num_files = redis_client.hlen(key)
        if num_files >= RecentFiles.MAX_STACK:
            oldest_file = redis_client.hkeys(key)[0]
            redis_client.hdel(key, oldest_file)
        data = json.dumps(info)
        redis_client.hset(key, file_id, data)
    
    @staticmethod
    def get_recent_files(user_id):
        """Get recent files"""
        key = f"recent_files:{user_id}"
        files = redis_client.hgetall(key)
        return files
