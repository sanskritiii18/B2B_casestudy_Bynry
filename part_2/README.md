# Solution:
The following database schema is designed based on the given requirements for an
inventory management platform.
Considering following point:
1) A company can have multiple warehouses, forming a one-to-many relationship.
2) Products can be stored in multiple warehouses with different quantities.
3) Since quantity depends on both product and warehouse, an Inventory table is required.
4) Suppliers can provide multiple products, and a product can be provided by multiple suppliers, forming a many-to-many relationship.
5) Inventory level changes must be tracked; therefore, an Inventory History table is needed.
6) Some products may be bundles composed of other products, which requires a Product Composition table.

# Main Entities
The following entities are required for the system:
•  Companies 
•  Warehouses 
•  Products 
•  Inventory 
•  Suppliers 
•  Inventory History 
•  Product Compositions (Bundles)


# Relationship 
•	Company → Warehouses
•	Product ↔ Warehouse (via Inventory)
•	Supplier ↔ Product
•	Inventory History
•	Product Bundles

# Tables
•	Companies
•	Warehouse 
•	Product
•	Supplier
•	Inventory
•	Inventory History
•	Supplier Product
•	Product Bundles

# Indexes

Products ->	Index on sku
Inventory->	Index on product_id
Inventory->	Index on warehouse_id
Supplier_Products->	Index on supplier_id
Inventory_History->	Index on product_id


# Design Decisions

- Inventory is stored separately because quantity depends on both product and warehouse.
- A junction table is used for supplier-product relationships to support many-to-many relationships.
- Inventory history is used to track stock changes for auditing.
- Product compositions allow bundles of products.

# Missing Requirements / Questions

- Can products belong to multiple companies?
- Can inventory go negative during reservations?
- Can multiple suppliers supply the same product with different prices?
- Should bundles automatically update inventory of component products?



# Tables
## Products Table
| Column Name | Data Type     | Constraints                 | Description                        |
| ----------- | ------------- | --------------------------- | ---------------------------------- |
| product_id  | INT           | Primary Key, Auto Increment | Unique identifier for product      |
| sku         | VARCHAR(100)  | UNIQUE, NOT NULL            | Stock Keeping Unit                 |
| name        | VARCHAR(255)  | NOT NULL                    | Product name                       |
| description | TEXT          | Optional                    | Product description                |
| price       | DECIMAL(10,2) | NOT NULL                    | Product price                      |
| created_at  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP   | Timestamp when product was created |

## companies Table
| Column Name | Data Type    | Constraints                 | Description                                   |
| ----------- | ------------ | --------------------------- | --------------------------------------------- |
| company_id  | INT          | Primary Key, Auto Increment | Unique identifier for each company            |
| name        | VARCHAR(255) | NOT NULL                    | Name of the company                           |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP   | Timestamp when the company record was created |


## Inventory Table

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| inventory_id | INT | Primary Key | Inventory record ID |
| product_id | INT | Foreign Key | References Products |
| warehouse_id | INT | Foreign Key | References Warehouses |
| quantity | INT | CHECK(quantity >= 0) | Available quantity |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |

## warehouse
| Column Name  | Data Type    | Constraints                         | Description                          |
| ------------ | ------------ | ----------------------------------- | ------------------------------------ |
| warehouse_id | INT          | Primary Key, Auto Increment         | Unique warehouse identifier          |
| company_id   | INT          | Foreign Key → Companies(company_id) | Company that owns the warehouse      |
| name         | VARCHAR(255) | NOT NULL                            | Name of the warehouse                |
| location     | VARCHAR(255) | Optional                            | Physical warehouse location          |
| created_at   | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP           | Timestamp when warehouse was created |


## Inventory History
| Column Name     | Data Type   | Constraints                            | Description                                   |
| --------------- | ----------- | -------------------------------------- | --------------------------------------------- |
| history_id      | INT         | Primary Key, Auto Increment            | Unique identifier for inventory change record |
| product_id      | INT         | Foreign Key → Products(product_id)     | Product whose inventory changed               |
| warehouse_id    | INT         | Foreign Key → Warehouses(warehouse_id) | Warehouse where change occurred               |
| change_quantity | INT         | NOT NULL                               | Amount added or removed                       |
| change_type     | VARCHAR(50) | NOT NULL                               | Type of change (purchase, sale, adjustment)   |
| changed_at      | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP              | Timestamp when change occurred                |


## supplier
| Column Name   | Data Type    | Constraints                 | Description                 |
| ------------- | ------------ | --------------------------- | --------------------------- |
| supplier_id   | INT          | Primary Key, Auto Increment | Unique supplier identifier  |
| name          | VARCHAR(255) | NOT NULL                    | Supplier name               |
| contact_email | VARCHAR(255) | Optional                    | Supplier contact email      |
| phone         | VARCHAR(50)  | Optional                    | Supplier phone number       |
| created_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP   | Supplier creation timestamp |



## supplier products 
| Column Name    | Data Type     | Constraints                          | Description                    |
| -------------- | ------------- | ------------------------------------ | ------------------------------ |
| supplier_id    | INT           | Foreign Key → Suppliers(supplier_id) | Supplier providing the product |
| product_id     | INT           | Foreign Key → Products(product_id)   | Product supplied               |
| supplier_price | DECIMAL(10,2) | Optional                             | Price offered by supplier      |
| lead_time_days | INT           | Optional                             | Delivery lead time             |



## Product bundles
| Column Name          | Data Type | Constraints                        | Description                            |
| -------------------- | --------- | ---------------------------------- | -------------------------------------- |
| bundle_product_id    | INT       | Foreign Key → Products(product_id) | Bundle product                         |
| component_product_id | INT       | Foreign Key → Products(product_id) | Product inside bundle                  |
| quantity             | INT       | NOT NULL                           | Quantity of component product required |
