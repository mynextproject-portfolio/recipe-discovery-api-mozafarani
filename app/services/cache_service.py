import json
import redis
from typing import List, Dict, Any, Optional


class CacheService:
    """Service for Redis caching operations"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = 24 * 60 * 60  # 24 hours in seconds
    
    def get_cached_search_results(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached search results for a query"""
        try:
            cache_key = f"mealdb_search:{query.lower().strip()}"
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            return None
            
        except (redis.RedisError, json.JSONDecodeError) as e:
            print(f"Cache get error: {e}")
            return None
    
    def cache_search_results(self, query: str, results: List[Dict[str, Any]]) -> bool:
        """Cache search results for a query"""
        try:
            cache_key = f"mealdb_search:{query.lower().strip()}"
            json_data = json.dumps(results)
            
            # Set with 24-hour TTL
            self.redis_client.setex(cache_key, self.default_ttl, json_data)
            return True
            
        except (redis.RedisError, TypeError) as e:
            print(f"Cache set error: {e}")
            return False
    
    def clear_cache(self) -> bool:
        """Clear all cached data"""
        try:
            self.redis_client.flushdb()
            return True
        except redis.RedisError as e:
            print(f"Cache clear error: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            info = self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except redis.RedisError as e:
            print(f"Cache stats error: {e}")
            return {}
