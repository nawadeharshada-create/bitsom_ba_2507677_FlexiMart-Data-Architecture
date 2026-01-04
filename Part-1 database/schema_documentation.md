#-----------Task 1.2: Database Schema Documentation.--------------#

Q.1 Entity-Relationship Description (Text Format)
#--------------CUSTOMERS--------------#
ENTITY: customers
Purpose: 
   Stores customer information.
Attributes:
   customer_id: Unique identifier (Primary Key)
   first_name: Customer's first name
   [list all attributes with descriptions]
Relationships:
   One customer can place MANY orders (1:M with orders table)

#--------------PRODUCTS--------------#
Entity: Products
Purpose: 
   Stores product catalog information available for sale.
Attributes:
   product_id: Unique product identifier
   product_name: Name of the product
   category: Product category(Electronics,Fashion,etc.)
   price: Selling price
   stock_quantity: Available stock units 
Relationships:
   One Product can appear in MANY order items
   products.product_id → order_items.product_id
   Relationship type: 1 : M


#--------------ORDERS--------------#
Entity: Orders
Purpose: 
   Stores high-level transaction information for customer purchases.
Attributes:
   order_id: Unique ordedr identifier
   customer_id(FK):References customer.customer_id
   order_date: Date of the transaction
   status: Order status(Completed,Pending)
Relationships:
   One order belongs to one customer 
   One order can have many order items 

#--------------ORDER_ITEMS--------------#
Entity: order_items
Purpose: 
   Stores line - item details for each order.
Attributes:
   order_items_id: Unique line-item identifier
   order_id (FK): References orders.order_id
   product_id (FK): References products.product_id
   quantity: Number of units purchased
   unit_price: Price per unit at time of sale
Relationships:
   Many order items belong to one order
   Many order items reference one product

Q.2 Normalization Explanation.
   This database schema is designed according to Third Normal Form (3NF) principles to ensure data integrity,
    minimize redundancy, and avoid anomalies.

1.Explain why this design is in 3NF (200-250 words)
First Normal Form(1NF):
   All tables have atomic values (no multi-valued or repeating fields).
   Each table has primary key that uniquely identifies records.
   Example:-
        Phone number and emails are stored as single values,not lists.

Second Normal Form(2NF):
   All non-key attributes are fully dependent on the primary key.
   Partial dependancies are eliminated.
   Example:-
        Product price and stock dependancy only on product_id,bot on any composite key.

Third Normal Form (3NF):
   There are no transitive dependancies.
   Non-key attributes depend only on the primary key, not on other non-key attributes.
   Example:-
        Customer city depends on cutomer_id ,not on email or phone.
        Product category depends on product_id, not on product name.


2.Identify functional dependencies
   customer_id → first_name, last_name, email, phone, city, registration_date

   product_id → product_name, category, price, stock_quantity

   order_id → customer_id, order_date, status

   order_item_id → order_id, product_id, quantity, unit_price


3.Explain how the design avoids update, insert, and delete anomalies.
   Insert Anomalies: New customers or products can be added without
                     requiring an order.

   Update Anomalies: Product price update occur in only one place 
                     (product table).

   Delete Anomalies: Deleting an order does not remove customer or
                      product data.


Q.3 Sample Data Representation

Show 2-3 sample records from each table in table format
Below are sample records from each table to demonstrate the structure and stored data.

#----------------customers (Sample Records)----------------#

| customer_id | first_name | last_name | email                    | phone      | city      | registration_date |
|------------ |----------- |-----------|--------------------------|------------|-----------|-------------------|
| C001        | Rahul      | Sharma    | rahul.sharma@gmail.com   | 9876543210 | Bangalore | 2023-01-15        |
| C002        | Priya      | Patel     | priya.patel@yahoo.com    | 9988776655 | Mumbai    | 2023-02-20        |
| C003        | Amit       | Kumar     | amit.kumar@missing.com   | 9765432109 | Delhi     | 2023-03-10        |


#---------------- products (Sample Records)-------------------#

| product_id | product_name       | category     | price  | stock_quantity |
|----------- |--------------------|--------------|--------|----------------|
| P001       | Samsung Galaxy S21 | Electronics  | 45999  | 150            |
| P002       | Nike Running Shoes | Fashion      | 3499   | 80             |
| P003       | Apple MacBook Pro  | Electronics  | 129999 | 45             |


#----------------- orders (Sample Records)-------------------#

| order_id | customer_id | order_date | status     |
|--------- |-------------|------------|------------|
| O001     | C001        | 2024-01-15 | Completed  |
| O002     | C002        | 2024-01-16 | Completed  |
| O003     | C003        | 2024-01-18 | Pending    |


#----------------- order_items (Sample Records)------------------#

| order_item_id | order_id | product_id | quantity | unit_price |
|-------------- |----------|------------|----------|------------|
| OI001         | O001     | P001       | 1        | 45999      |
| OI002         | O002     | P004       | 2        | 2999       |
| OI003         | O003     | P002       | 1        | 3499       |


Conclusion:-
The FlexiMart database schema was created successfully using MySQL. It contains tables for customers, products, orders, and order items, all connected using proper keys. The schema follows 3NF, which helps avoid duplicate data and keeps the database organized. The data loaded through the ETL pipeline was checked in MySQL Workbench and found to be correct.