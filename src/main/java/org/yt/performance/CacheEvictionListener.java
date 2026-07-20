package com.example.domain.cache;

import org.springframework.cache.Cache;
import org.springframework.cache.interceptor.CacheOperationEvent;
import org.springframework.stereotype.Component;

@Component
public class CacheEvictionListener {

    public void onCacheEntryRemoved(CacheOperationEvent event) {
        Cache cache = event.getCache();
        String cacheName = cache.getName();

        // Implement logic to invalidate stale cache keys based on the cache name or other criteria.
        if (cacheName.equals("productCache")) {
            // Example: Invalidate all entries in 'productCache' that are older than a certain time
            cache.evictAllEntriesBasedOnAgeThreshold();
        } else if (cacheName.equals("userCache")) {
            // Example: Invalidate specific keys based on some condition
            String[] keysToInvalidate = {"12345", "67890"};
            for (String key : keysToInvalidate) {
                cache.evict(key);
            }
        }

        // You can add more conditions and actions as needed.
    }

    private void evictAllEntriesBasedOnAgeThreshold() {
        // Implement logic to find all entries older than a certain time threshold
        // This is just an example placeholder method
    }
}

In this code:

- The `CacheEvictionListener` class listens for events when cache entries are removed.
- It checks the name of the cache and performs specific actions based on that name.
- Example methods like `evictAllEntriesBasedOnAgeThreshold()` are placeholders where you can implement your logic to invalidate stale cache keys.

You would need to integrate this listener with Spring's caching infrastructure, typically through configuration or annotations.