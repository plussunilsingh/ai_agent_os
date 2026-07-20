package com.example.repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.List;

@Repository
public class JdbcBatchRepository {

    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public JdbcBatchRepository(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }

    /**
     * Batch insert data into the database using JDBC batch operations.
     *
     * @param items the list of objects to be inserted.
     */
    public void batchInsert(List<Item> items) {
        String sql = "INSERT INTO item (id, name, description) VALUES (?, ?, ?)";
        
        // Prepare the batch statement
        jdbcTemplate.batchUpdate(sql, new BatchPreparedStatementSetter() {
            @Override
            public void setValues(PreparedStatement ps, int i) throws SQLException {
                Item item = items.get(i);
                ps.setInt(1, item.getId());
                ps.setString(2, item.getName());
                ps.setString(3, item.getDescription());
            }

            @Override
            public int getBatchSize() {
                return items.size();
            }
        });
    }

    /**
     * A simple data transfer object (DTO) representing an item.
     */
    static class Item {
        private int id;
        private String name;
        private String description;

        // Getters and setters

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }
    }
}

### Explanation:

1. **Dependencies and Imports**:
   - `org.springframework.jdbc.core.BatchPreparedStatementSetter` is used to handle batch operations.
   - `org.springframework.jdbc.core.JdbcTemplate` provides a high-level abstraction for executing SQL queries.

2. **Constructor Injection**:
   - The `DataSource` is injected via constructor, which is then used to create the `JdbcTemplate`.

3. **Batch Insert Method (`batchInsert`)**:
   - This method takes a list of `Item` objects and inserts them into the database using batch operations.
   - The SQL statement is defined as `"INSERT INTO item (id, name, description) VALUES (?, ?, ?)"`.
   - A `BatchPreparedStatementSetter` is used to set values for each item in the list.

4. **Performance Considerations**:
   - Batch operations are known to be highly efficient and can significantly reduce the number of round-trips to the database.
   - The `getBatchSize()` method returns the size of the batch, which helps in optimizing performance.

5. **Item Class**:
   - A simple DTO class `Item` is defined with basic getters and setters for demonstration purposes.

### Notes:

- Ensure that your table schema (`item`) matches the columns in the SQL statement.
- For production use, consider adding error handling to manage exceptions during batch insertion.
- The performance optimization of under 5ms can be achieved by fine-tuning the database configuration, indexing strategies, and network latency.