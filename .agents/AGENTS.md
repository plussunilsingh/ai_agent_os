# Backend Build Guidelines

Whenever the user asks you to build, test, or verify the backend application, you MUST perform the following validation checklist:

1. **Spotless Code Formatting Check**:
   * Run `./gradlew spotlessCheck` to verify Java code formatting.
   * If there are formatting errors, run `./gradlew spotlessApply` to format the code automatically.
2. **Static Analysis (Checkstyle & PMD)**:
   * Do not skip static analysis checks. Ensure `config/checkstyle/checkstyle.xml` and `config/pmd/pmd-rules.xml` exist and are valid.
   * Run `./gradlew check` or `./gradlew build` to execute Checkstyle and PMD tasks.
3. **Unit & Integration Tests**:
   * Run `./gradlew test` to execute all JUnit test suites and ensure 100% test success.
4. **Hardcoded Versions**:
   * Ensure all dependency versions inside `build.gradle` are hardcoded/pinned to specific versions for production go-live release. Avoid using dynamic or unpinned versions.

## Lessons Learned & Common Issues

* **Checkstyle & PMD Validation**:
  * Checkstyle ruleset `config/checkstyle/checkstyle.xml` must exist. Do not delete it, otherwise builds will crash on CI.
  * PMD version is `7.0.0`. Do not use deprecated rules like `ExcessiveMethodLength` or `ExcessiveClassLength` in `config/pmd/pmd-rules.xml` since they will fail PMD parser initialization.
* **Strict Generic Return Typing**:
  * Maintain strict compile-time types for REST controllers and services. Avoid returning `ApiResponse<Object>` or raw maps (`Map<String, Object>`) for collection results.
  * Use Java records in `com.bn.admin.dto.ResponseRecords` (e.g., `CustomerListResponse`, `MaterialListResponse`) and wrap lists with wildcard lists `List<?>` when dynamically mapping batch details.
* **Database Connection Pooling**:
  * For production, always use optimized pool configurations (e.g. HikariCP settings in `application-prod.properties` with `maximum-pool-size=20`).

