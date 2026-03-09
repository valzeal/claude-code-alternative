"""
Claude Code Alternative - Cache Manager (Phase 3)
Performance optimization through intelligent caching
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from functools import wraps
import threading


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    timestamp: float
    ttl: int  # Time to live in seconds
    hit_count: int = 0
    size_bytes: int = 0


class CacheManager:
    """Thread-safe cache manager with LRU eviction and TTL support"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initialize cache manager

        Args:
            max_size: Maximum number of entries in cache
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: Dict[str, float] = {}  # Track access time for LRU
        self.lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'current_size': 0,
            'total_bytes': 0
        }
    
    def _generate_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate cache key from function name and arguments"""
        key_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': str(sorted(kwargs.items()))
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def _get_size(self, value: Any) -> int:
        """Estimate memory size of value in bytes"""
        try:
            return len(json.dumps(value))
        except:
            return len(str(value))
    
    def _evict_expired(self) -> int:
        """Evict expired entries"""
        evicted = 0
        current_time = time.time()
        
        with self.lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time - entry.timestamp > entry.ttl
            ]
            
            for key in expired_keys:
                self._remove_entry(key)
                evicted += 1
        
        return evicted
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry"""
        if not self.access_order:
            return
        
        with self.lock:
            # Find least recently used key
            lru_key = min(self.access_order, key=self.access_order.get)
            self._remove_entry(lru_key)
            self.stats['evictions'] += 1
    
    def _remove_entry(self, key: str) -> None:
        """Remove entry from cache"""
        if key in self.cache:
            entry = self.cache[key]
            self.stats['current_size'] -= 1
            self.stats['total_bytes'] -= entry.size_bytes
            del self.cache[key]
            if key in self.access_order:
                del self.access_order[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            # Evict expired entries first
            self._evict_expired()
            
            if key not in self.cache:
                self.stats['misses'] += 1
                return None
            
            entry = self.cache[key]
            
            # Check if expired
            if time.time() - entry.timestamp > entry.ttl:
                self._remove_entry(key)
                self.stats['misses'] += 1
                return None
            
            # Update access time and hit count
            entry.hit_count += 1
            self.access_order[key] = time.time()
            self.stats['hits'] += 1
            
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        current_time = time.time()
        size = self._get_size(value)
        
        with self.lock:
            # Evict expired entries
            self._evict_expired()
            
            # If key exists, update it
            if key in self.cache:
                old_entry = self.cache[key]
                self.stats['total_bytes'] -= old_entry.size_bytes
            else:
                # Check if we need to evict LRU
                if len(self.cache) >= self.max_size:
                    self._evict_lru()
            
            # Create new entry
            entry = CacheEntry(
                key=key,
                value=value,
                timestamp=current_time,
                ttl=ttl,
                size_bytes=size
            )
            
            self.cache[key] = entry
            self.access_order[key] = current_time
            self.stats['current_size'] = len(self.cache)
            self.stats['total_bytes'] += size
    
    def invalidate(self, key: str) -> None:
        """Invalidate cache entry"""
        with self.lock:
            self._remove_entry(key)
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            self.access_order.clear()
            self.stats['current_size'] = 0
            self.stats['total_bytes'] = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            hit_rate = (
                self.stats['hits'] / (self.stats['hits'] + self.stats['misses'])
                if (self.stats['hits'] + self.stats['misses']) > 0
                else 0.0
            )
            
            return {
                **self.stats,
                'hit_rate': f"{hit_rate:.2%}",
                'max_size': self.max_size
            }


def cached(ttl: Optional[int] = None, cache_manager: Optional[CacheManager] = None):
    """
    Decorator to cache function results

    Args:
        ttl: Time to live in seconds (uses cache default if not specified)
        cache_manager: Custom cache manager instance
    """
    if cache_manager is None:
        cache_manager = CacheManager()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_manager._generate_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            result = cache_manager.get(key)
            if result is not None:
                return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl)
            
            return result
        
        # Attach cache manager to function for stats access
        wrapper.cache_manager = cache_manager
        return wrapper
    
    return decorator


class CodeAnalysisCache:
    """Specialized cache for code analysis results"""
    
    def __init__(self, max_size: int = 500, default_ttl: int = 1800):
        """
        Initialize code analysis cache

        Args:
            max_size: Maximum number of cached analyses
            default_ttl: Default TTL in seconds (30 minutes)
        """
        self.cache = CacheManager(max_size=max_size, default_ttl=default_ttl)
    
    def get_analysis(self, code: str, language: str) -> Optional[Dict]:
        """Get cached code analysis"""
        key = self._generate_code_key(code, language)
        return self.cache.get(key)
    
    def set_analysis(self, code: str, language: str, analysis: Dict, ttl: Optional[int] = None) -> None:
        """Cache code analysis result"""
        key = self._generate_code_key(code, language)
        self.cache.set(key, analysis, ttl)
    
    def _generate_code_key(self, code: str, language: str) -> str:
        """Generate cache key for code analysis"""
        # Remove whitespace normalization for code
        normalized_code = '\n'.join(line.rstrip() for line in code.split('\n'))
        key_data = f"{language}:{normalized_code}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def invalidate_code(self, code: str, language: str) -> None:
        """Invalidate specific code analysis"""
        key = self._generate_code_key(code, language)
        self.cache.invalidate(key)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_stats()


# Example usage
if __name__ == "__main__":
    # Example 1: Using cache manager directly
    cache = CacheManager(max_size=100, default_ttl=300)
    
    cache.set("user:123", {"name": "John", "age": 30})
    user_data = cache.get("user:123")
    print("Cached user data:", user_data)
    
    # Example 2: Using decorator
    @cached(ttl=60)
    def expensive_computation(n: int) -> int:
        """Simulate expensive computation"""
        import time
        time.sleep(0.1)  # Simulate work
        return sum(range(n))
    
    # First call - computes
    import time
    start = time.time()
    result1 = expensive_computation(1000)
    time1 = time.time() - start
    
    # Second call - from cache
    start = time.time()
    result2 = expensive_computation(1000)
    time2 = time.time() - start
    
    print(f"\nFirst call: {time1:.3f}s (computed)")
    print(f"Second call: {time2:.3f}s (cached)")
    print(f"Speedup: {time1/time2:.1f}x")
    print(f"\nCache stats: {expensive_computation.cache_manager.get_stats()}")
    
    # Example 3: Code analysis cache
    code_cache = CodeAnalysisCache()
    
    python_code = '''
def hello():
    print("Hello, World!")
'''
    
    # Cache and retrieve
    code_cache.set_analysis(python_code, 'python', {
        'lines': 3,
        'functions': 1,
        'complexity': 1
    })
    
    cached_analysis = code_cache.get_analysis(python_code, 'python')
    print(f"\nCached analysis: {cached_analysis}")
    print(f"Code analysis cache stats: {code_cache.get_stats()}")
