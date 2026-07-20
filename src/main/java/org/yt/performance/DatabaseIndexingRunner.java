package com.example.domain6.performance.cacheengine;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;
import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.Query;
import java.util.List;

@Component
public class DatabaseIndexingRunner implements ApplicationRunner {

    private final EntityManagerFactory entityManagerFactory;

    public DatabaseIndexingRunner() {
        this.entityManagerFactory = Persistence.createEntityManagerFactory("examplePersistenceUnit");
    }

    @Override
    public void run(ApplicationArguments args) throws Exception {
        // Ensure indexes are created on startup
        createIndexes();
    }

    private void createIndexes() {
        EntityManager entityManager = entityManagerFactory.createEntityManager();
        entityManager.getTransaction().begin();

        try {
            // Indexing Entity1
            createIndexOnEntity1(entityManager);

            // Indexing Entity2
            createIndexOnEntity2(entityManager);

            // Commit the transaction to apply indexes
            entityManager.getTransaction().commit();
        } finally {
            if (entityManager.getTransaction().isActive()) {
                entityManager.getTransaction().rollback();
            }
            entityManager.close();
        }
    }

    private void createIndexOnEntity1(EntityManager entityManager) {
        Query query = entityManager.createNativeQuery(
                "CREATE INDEX idx_entity1_column1 ON Entity1(column1);"
        );
        query.executeUpdate();
    }

    private void createIndexOnEntity2(EntityManager entityManager) {
        Query query = entityManager.createNativeQuery(
                "CREATE INDEX idx_entity2_column2 ON Entity2(column2);"
        );
        query.executeUpdate();
    }
}

### Explanation:
- **Dependencies**: The code uses Spring Boot's `ApplicationRunner` to run tasks on application startup. It leverages JPA for database operations.
- **Index Creation**: Two methods, `createIndexOnEntity1` and `createIndexOnEntity2`, are used to create B-tree indexes on specific columns of the respective entities (`Entity1` and `Entity2`). These methods use native SQL queries to ensure high-speed index creation.
- **Transaction Management**: A transaction is started and committed after executing the SQL queries. If an error occurs, it rolls back the transaction to avoid leaving the database in an inconsistent state.

### Notes:
- Ensure that your persistence unit name (`examplePersistenceUnit`) matches the configuration in `application.properties` or `persistence.xml`.
- Replace `Entity1`, `Entity2`, and their column names with actual entity and column names from your application.
- Adjust the index creation logic based on specific requirements and database constraints.

This code is designed to be production-ready, focusing on performance optimization through efficient index creation during startup.