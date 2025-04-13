# MediSupply ERD and Database Architecture

## 1. ERD Diagram
![ERD Diagram](images/erd_diagram.png)

## 2. Overview
This document provides a detailed explanation of the Entity-Relationship Diagram (ERD) for the MediSupply project. The ERD outlines the structure of the database and shows how various entities interrelate in order to support the project use cases. The design ensures that all the use cases—including purchase order creation, approval/rejection, order status updates, and order viewing—are supported by a robust and scalable database architecture.

## 3. Entities and Attributes

### 3.1 PurchaseOrder
- **Description:** Represents a purchase order initiated by Hospital Staff.
- **Key Attributes:**
  - **order_id:** A unique identifier for each purchase order.
  - **date_created:** Timestamp when the order was created.
  - **status:** Indicates the current state of the order (e.g., "Pending", "Approved", "Rejected", "Shipped", "Delivered").
  - **created_by:** Foreign key referencing the User who created the order.
  - **total_amount:** (Optional) Calculated field based on the sum of the prices of the items in the order.

### 3.2 OrderItem
- **Description:** Represents each item within a purchase order.
- **Key Attributes:**
  - **item_id:** A unique identifier for each order item.
  - **description:** Details about the supply item.
  - **quantity:** The number of units for that item.
  - **price:** The cost per unit of the item.
  - **order_id:** Foreign key linking back to the related PurchaseOrder, establishing a one-to-many relationship.

### 3.3 User
- **Description:** Represents users in the system, including Hospital Staff, Purchasing Managers, Suppliers, and Administrators.
- **Key Attributes:**
  - **user_id:** A unique identifier for each user.
  - **username:** The login name.
  - **password:** The user’s password (stored securely using appropriate encryption/hashing).
  - **role:** Specifies the user’s role (e.g., "Hospital Staff", "Purchasing Manager", "Supplier", "Administrator").
  - **email:** User's contact email, which can be used for notifications.

### 3.4 Additional Considerations
- **Relationships:**
  - **PurchaseOrder to OrderItem:**  
    A single purchase order can contain multiple order items (one-to-many relationship). This ensures that each purchase order can fully list the items being requested.
  - **PurchaseOrder to User:**  
    Each order is created by one user (Hospital Staff) but can be reviewed by another user (Purchasing Manager). This relationship is reflected by the `created_by` attribute in the PurchaseOrder entity.
  - **User Role Differentiation:**  
    Although all system users are stored in one `User` entity, the attribute `role` differentiates functionality. Additional role-specific data may be added via extension tables or additional attributes if needed.

## 4. How the ERD Supports Use Cases
- **Creating Purchase Orders:**  
  The entities PurchaseOrder and OrderItem capture all necessary details for the creation process. The relationship between these entities allows Hospital Staff to enter multiple items and details with a single order reference.
- **Approval Process:**  
  By connecting a PurchaseOrder record to the User who created it (and later modifying its status), the system facilitates a clear audit trail and enables Purchasing Managers to review and provide feedback.
- **Order Status Updates:**  
  Suppliers can update the `status` field of a PurchaseOrder. This change is automatically reflected across system modules, ensuring that both Hospital Staff and Purchasing Managers are kept informed.
- **Viewing Orders:**  
  Querying the database by status or by the creator (user_id) allows each role to easily access the orders relevant to them, fulfilling the various “view orders” use cases.

## 5. Future Enhancements
- **Additional Attributes:**  
  Future versions may incorporate more detailed attributes such as shipping information, timestamps for status updates, or audit logs.
- **Normalization:**  
  The current design follows normalization best practices to reduce redundancy and improve data integrity.

*End of ERD Documentation*
