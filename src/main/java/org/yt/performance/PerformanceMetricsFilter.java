package com.example.filters;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.concurrent.atomic.AtomicLong;

/**
 * PerformanceMetricsFilter measures the execution time of HTTP endpoints and ensures they meet sub-20ms SLA.
 */
public class PerformanceMetricsFilter implements Filter {

    private final AtomicLong metricCounter = new AtomicLong(0);

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        // Initialization code if needed, not typically required for this simple filter
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        long startTime = System.currentTimeMillis();

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        String url = httpRequest.getRequestURI();
        // Optional: Log or record the URL for analysis

        chain.doFilter(request, response);

        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;

        if (executionTime >= 20) {
            throw new ServletException("HTTP Endpoint '" + url + "' took longer than 20ms to execute. Execution time: " + executionTime + "ms");
        }

        metricCounter.incrementAndGet();

    }

    @Override
    public void destroy() {
        // Cleanup code if needed, not typically required for this simple filter
    }
}

### Explanation:
1. **Initialization**: The `init` method is implemented but left empty as no specific initialization is necessary.
2. **Filter Logic**:
   - The `doFilter` method measures the execution time of the HTTP endpoint by capturing the start and end times.
   - It then checks if the execution time exceeds 20ms, throwing a `ServletException` with an appropriate message if it does.
3. **Metrics Collection**: An atomic counter (`metricCounter`) is used to keep track of how many requests have been processed through this filter.
4. **Cleanup**: The `destroy` method is implemented but left empty as no cleanup is typically required for this simple filter.

### Usage:
- This filter can be configured in the web application's deployment descriptor (web.xml) or via annotations like `@WebFilter`.

<filter>
    <filter-name>PerformanceMetricsFilter</filter-name>
    <filter-class>com.example.filters.PerformanceMetricsFilter</filter-class>
</filter>

<filter-mapping>
    <filter-name>PerformanceMetricsFilter</filter-name>
    <url-pattern>/api/*</url-pattern>
</filter-mapping>

This setup ensures that all requests to URLs matching the specified pattern are filtered, and any request taking more than 20ms will be flagged.