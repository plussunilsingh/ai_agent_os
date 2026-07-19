package org.yt.integration;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest
public class FullBusinessFlowTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MaterialIntakeService materialIntakeService;

    @MockBean
    private InventoryService inventoryService;

    @MockBean
    private DispatchSalesService dispatchSalesService;

    @BeforeEach
    public void setUp() {
        // Setup any necessary mocks or initial states if needed.
    }

    @Test
    public void testMaterialIntakeEndpoint() throws Exception {
        mockMvc.perform(post("/material-intake")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"quantity\": 100, \"productCode\": \"A123\"}"))
                .andExpect(status().isOk());
    }

    @Test
    public void testInventoryUpdateEndpoint() throws Exception {
        mockMvc.perform(get("/inventory-update/{productCode}", "A123")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content().string("Stock updated for product A123"));
    }

    @Test
    public void testDispatchSalesEndpoint() throws Exception {
        mockMvc.perform(post("/dispatch-sales")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"quantity\": 50, \"productCode\": \"A123\"}"))
                .andExpect(status().isOk())
                .andExpect(content().string("Product A123 dispatched successfully"));
    }
}

### Explanation:
- **@WebMvcTest**: This annotation is used to create a Spring Boot test context that includes only the `@Controller` classes and their required beans.
- **MockMvc**: Used to perform HTTP requests against the application under test.
- **@MockBean**: Mocks for services are created using this annotation. Replace `MaterialIntakeService`, `InventoryService`, and `DispatchSalesService` with actual service implementations if necessary.

### Note:
- Ensure that the endpoints (`/material-intake`, `/inventory-update/{productCode}`, `/dispatch-sales`) exist in your application.
- The content of the requests is simplified for demonstration. Adjust according to your actual requirements.
- Add any specific logic or mock behavior as needed for each service method using `@MockBean`.