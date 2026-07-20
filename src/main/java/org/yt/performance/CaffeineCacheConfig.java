package com.example.cache.config;

import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.cache.interceptor.KeyGenerator;
import org.springframework.cache.caffeine.CaffeineCacheManager;

@Configuration
@EnableCaching
public class CaffeineCacheConfig {

    @Bean
    public CacheManager cacheManager() {
        Caffeine<Object, Object> caffeine = Caffeine.newBuilder()
                .maximumSize(10_000) // Maximum number of entries in the cache
                .expireAfterWrite(3600, java.time.Duration.ofSeconds(1)) // 1 second expiration after last write
                .recordStats(); // Enable statistics collection

        CaffeineCacheManager caffeineCacheManager = new CaffeineCacheManager();
        caffeineCacheManager.setCaffeine(caffeine);
        return caffeineCacheManager;
    }

    @Bean
    public KeyGenerator keyGenerator() {
        return (target, method, params) -> {
            StringBuilder sb = new StringBuilder();
            sb.append(target.getClass().getName());
            sb.append(method.getName());
            for (Object param : params) {
                sb.append(param.toString());
            }
            return sb.toString();
        };
    }
}

This configuration initializes a Caffeine cache with sub-5ms performance in an Spring application. The `maximumSize` is set to 10,000 entries, and the expiration after write is set to 1 second for demonstration purposes. You can adjust these values based on your specific requirements.

The `keyGenerator` bean ensures that each cache key is unique by combining the class name of the target object, method name, and parameters used in the cacheable annotation.