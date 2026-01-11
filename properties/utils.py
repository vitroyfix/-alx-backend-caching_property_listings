from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Retrieve all properties from cache or database.
    Cache for 1 hour (3600 seconds).
    """
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        logger.info("Properties retrieved from cache")
        return cached_properties
    
    logger.info("Properties retrieved from database")
    queryset = list(Property.objects.all())
    cache.set('all_properties', queryset, 3600)
    
    return queryset


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    try:
        redis_conn = get_redis_connection('default')
        info = redis_conn.info('stats')
        
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': round(hit_ratio, 2)
        }
        
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0,
            'error': str(e)
        }
