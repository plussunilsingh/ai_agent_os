package com.example.domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class FastAnalyticsQueryDTO {

    private String queryId;

    private Long startTime;

    private Long endTime;

    private Integer timeBucketSize;

    private List<String> metrics;

    private Map<String, String> dimensions;

    private boolean isCacheEnabled;

    private int cacheTtlSeconds;

    private boolean isAggregationRequired;

    private boolean isRealTimeQuery;

    public FastAnalyticsQueryDTO(String queryId, Long startTime, Long endTime, Integer timeBucketSize,
                                 List<String> metrics, Map<String, String> dimensions, boolean isCacheEnabled,
                                 int cacheTtlSeconds, boolean isAggregationRequired, boolean isRealTimeQuery) {
        this.queryId = queryId;
        this.startTime = startTime;
        this.endTime = endTime;
        this.timeBucketSize = timeBucketSize;
        this.metrics = metrics;
        this.dimensions = dimensions;
        this.isCacheEnabled = isCacheEnabled;
        this.cacheTtlSeconds = cacheTtlSeconds;
        this.isAggregationRequired = isAggregationRequired;
        this.isRealTimeQuery = isRealTimeQuery;
    }

    // Add any additional methods or logic here if necessary
}

### Explanation:
- **Lombok Annotations**:
  - `@Data`: Generates getters, setters, and constructors.
  - `@NoArgsConstructor` and `@AllArgsConstructor`: Generate a no-arg constructor and a constructor with all fields as parameters respectively.
  - `@Builder`: Enables builder pattern for object creation.

- **Fields**:
  - `queryId`: A unique identifier for the query.
  - `startTime`, `endTime`: Timestamps defining the time range of the query.
  - `timeBucketSize`: The size of each time bucket for aggregation.
  - `metrics`: List of metrics to be aggregated.
  - `dimensions`: Map of dimensions used in the query, where keys are dimension names and values are their corresponding types or configurations.
  - `isCacheEnabled`: Boolean flag indicating whether caching is enabled for this query.
  - `cacheTtlSeconds`: Time-to-live (TTL) value for cache entries if caching is enabled.
  - `isAggregationRequired`: Flag to indicate if aggregation of raw data is needed.
  - `isRealTimeQuery`: Flag to differentiate between real-time and historical queries.

### Usage Example:
FastAnalyticsQueryDTO query = FastAnalyticsQueryDTO.builder()
        .queryId("12345")
        .startTime(1609459200000L) // 2021-01-01T00:00:00Z
        .endTime(1609545600000L)   // 2021-01-02T00:00:00Z
        .timeBucketSize(3600)
        .metrics(List.of("metric1", "metric2"))
        .dimensions(Map.of("dimension1", "type1", "dimension2", "type2"))
        .isCacheEnabled(true)
        .cacheTtlSeconds(3600) // 1 hour
        .isAggregationRequired(true)
        .isRealTimeQuery(false)
        .build();

This DTO is designed to be flexible and can be used for various types of analytics queries, ensuring that all necessary parameters are captured efficiently.