package com.example.cacheperf;

import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.repository.core.support.RepositoryFactorySupport;

import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
public class CaffeineCachePerformanceTest {

    private static final long TIMEOUT = 5L; // milliseconds

    @Autowired
    private RepositoryFactorySupport repositoryFactorySupport;

    @BeforeAll
    public static void setup() {
        Cache<String, Object> cache = Caffeine.newBuilder()
                .maximumSize(10_000)
                .expireAfterWrite(TIMEOUT, TimeUnit.MILLISECONDS)
                .build();

        // Assuming the repository is a simple JPA entity repository and we are using it to populate the cache
        // Populate the cache with some data (this is just an example and should be adapted based on your actual use case)
        for (int i = 0; i < 1000; i++) {
            String key = "key" + i;
            Object value = new Object(); // Replace this with a real entity
            cache.put(key, value);
        }
    }

    @Test
    public void testCacheHitLatency() throws InterruptedException {
        Cache<String, Object> cache = Caffeine.newBuilder()
                .maximumSize(10_000)
                .expireAfterWrite(TIMEOUT, TimeUnit.MILLISECONDS)
                .build();

        // Simulate a repository call that hits the cache
        String keyToTest = "key50"; // Adjust this based on your cache population logic

        assertTimeoutPreemptively(
                java.time.Duration.ofMillis(TIMEOUT),
                () -> {
                    Object valueFromCache = cache.getIfPresent(keyToTest);
                    assertTrue(valueFromCache != null, "Value should be present in the cache");
                }
        );
    }
}

### Explanation:
1. **Setup**: The `@BeforeAll` method initializes a Caffeine cache with a maximum size of 10,000 entries and an expiration time of 5ms after write. It populates the cache with 1,000 keys.
2. **Test Method**: The `testCacheHitLatency` method tests if a cache hit is performed within 5 milliseconds. It uses `assertTimeoutPreemptively` to ensure that any operation exceeding this time limit will fail the test.

### Notes:
- Ensure you have the Caffeine library in your classpath.
- Adjust the key and value logic based on your actual use case.
- This example assumes a simple entity repository, replace with actual entities and repositories as needed.