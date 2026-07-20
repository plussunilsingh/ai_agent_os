package com.example.orderfulfillment.dto;

import lombok.Data;
import java.util.Date;

@Data
public class CustomerDTO {

    private Long id;

    private String firstName;

    private String lastName;

    private String email;

    private String phoneNumber;

    private Date dateOfBirth;

    private String addressLine1;

    private String addressLine2;

    private String city;

    private String state;

    private String postalCode;

    private String country;

    private Date accountCreationDate;

    private boolean isSubscribedToNewsletter;

    // Optional: For Hibernate or other ORM frameworks
    @javax.persistence.Id
    private Long customerIdHibernate;

    public CustomerDTO() {
        // Default constructor for deserialization and other use cases
    }

    public CustomerDTO(Long id, String firstName, String lastName, String email, String phoneNumber,
                      Date dateOfBirth, String addressLine1, String addressLine2, String city, String state,
                      String postalCode, String country, Date accountCreationDate, boolean isSubscribedToNewsletter) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.phoneNumber = phoneNumber;
        this.dateOfBirth = dateOfBirth;
        this.addressLine1 = addressLine1;
        this.addressLine2 = addressLine2;
        this.city = city;
        this.state = state;
        this.postalCode = postalCode;
        this.country = country;
        this.accountCreationDate = accountCreationDate;
        this.isSubscribedToNewsletter = isSubscribedToNewsletter;
    }
}

### Explanation:
1. **Lombok @Data Annotation**: This annotation simplifies the class by auto-generating the `getter`, `setter`, `toString`, `equals`, and `hashCode` methods.
2. **Fields**:
   - `id`: Unique identifier for the customer.
   - `firstName`, `lastName`, `email`, `phoneNumber`: Basic contact details.
   - `dateOfBirth`: Date of birth.
   - `addressLine1`, `addressLine2`, `city`, `state`, `postalCode`, `country`: Address information.
   - `accountCreationDate`: Date when the customer account was created.
   - `isSubscribedToNewsletter`: Boolean flag to indicate if the customer is subscribed to the newsletter.

3. **Optional Hibernate Id Field**: This field is optional and can be used for integration with an ORM like Hibernate, where it would be annotated with `@Id`.

4. **Default Constructor**: Added a default constructor for deserialization or other use cases.
5. **Parameterized Constructor**: Added a parameterized constructor to facilitate object creation directly from database records.

This DTO is designed to be clean and production-ready, ensuring that all fields are properly encapsulated and easily accessible through Lombok annotations.