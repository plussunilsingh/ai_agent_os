package com.example.domain.performance.cache.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * DTO class to encapsulate the result of batch update operations.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BatchUpdateResultDTO {

    /**
     * The number of rows affected by the batch update operation.
     */
    private int updatedRowsCount;

    /**
     * A list of individual update results, each representing the number of rows affected by a single SQL statement in the batch.
     */
    private List<Integer> individualUpdateCounts;

    /**
     * A boolean flag indicating whether any updates were successful (i.e., no exceptions occurred during execution).
     */
    private boolean isSuccessful;

    /**
     * Any exception encountered during the batch update operation, if applicable.
     */
    private Exception exception;
}

This `BatchUpdateResultDTO` class provides a structured way to handle and report the results of bulk database operations. It includes fields for the total number of rows updated, individual counts for each SQL statement in a batch, a success flag, and any exceptions that might have occurred.

### Explanation:
- **updatedRowsCount**: This field holds the total number of rows affected by all statements in the batch.
- **individualUpdateCounts**: A list where each element represents the number of rows updated by an individual SQL statement within the batch. This is useful for debugging or logging purposes to understand which specific update statements were successful and how many rows they impacted.
- **isSuccessful**: A boolean that indicates whether all operations in the batch were successful without any exceptions.
- **exception**: If there was an exception during the execution of the batch, this field will hold it. This is useful for error handling and logging.

This DTO can be used in scenarios where you need to provide detailed feedback about the outcome of a batch update operation, ensuring that both success and failure cases are properly handled and reported.