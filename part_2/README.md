Solution:
The following database schema is designed based on the given requirements for an
inventory management platform.
Considering following point:
1) A company can have multiple warehouses, forming a one-to-many relationship.
2) Products can be stored in multiple warehouses with different quantities.
3) Since quantity depends on both product and warehouse, an Inventory table is required.
4) Suppliers can provide multiple products, and a product can be provided by multiple suppliers, forming a many-to-many relationship.
5) Inventory level changes must be tracked; therefore, an Inventory History table is needed.
6) Some products may be bundles composed of other products, which requires a Product Composition table.

Main Entities
The following entities are required for the system:
•  Companies 
•  Warehouses 
•  Products 
•  Inventory 
•  Suppliers 
•  Inventory History 
•  Product Compositions (Bundles)


Relationship 
•	Company → Warehouses
•	Product ↔ Warehouse (via Inventory)
•	Supplier ↔ Product
•	Inventory History
•	Product Bundles

 Tables
•	Companies
•	Warehouse 
•	Product
•	Supplier
•	Inventory
•	Inventory History
•	Supplier Product
•	Product Bundles

Indexes

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

