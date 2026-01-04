#-------------Task 3.1: Star Schema Design Documentation----------------#
#---------------------Section 1: Schema Overview------------------------#

Fleximart requires a data warehouse to analyze historical sales patterns.
A "Star Schema" is chosen because it is simple, efficient, and optimized for 
analytical quires.

##--FACT TABLE: fact_sales

Grain: One row per product per order line item
Business Process: Sales transactions

Measures (Numeric Facts):
- quantity_sold: Number of units sold
- unit_price: Price per unit at time of sale
- discount_amount: Discount applied
- total_amount: Final amount (quantity × unit_price - discount)

Foreign Keys:
- date_key → dim_date
- product_key → dim_product
- customer_key → dim_customer

-------------------------------------------------------------------------

##--DIMENSION TABLE: dim_date

Purpose:
     Date dimension for time-based analysis.
Type:
     Conformed dimension
Attributes:
- date_key (PK): Surrogate key (integer, format: YYYYMMDD)
- full_date: Actual date
- day_of_week: Monday, Tuesday, etc.
- month: 1-12
- month_name: January, February, etc.
- quarter: Q1, Q2, Q3, Q4
- year: 2023, 2024, etc.
- is_weekend: Boolean

-------------------------------------------------------------------------

##--DIMENSION TABLE: dim_product

Purpose:
      Product - Level analysis.
Attributes:
- product_key (PK): Surrogate key
- product_id: Natural product identifier
- product_name: Name of the product
- category: Electronics, Furniture, etc.
- brand: Manufacturer brand 
- storage_capacity: Storage specification
- ram: RAM specification

-------------------------------------------------------------------------

##--DIMENSION TABLE: dim_customer

Purpose:
     Customer - based analysis
Attributes:
- customer_key (PK): Surrogate key
- customer_id: Natural customer identifier
- customer_name: Full name
- city: Customer city
- state: Customer state 
- country: Customer country
- customer_sengment: Retail / Corporate

-------------------------------------------------------------------------
#-------------------- Section 2: Design Decisions-----------------------#

1. Why you chose this granularity (transaction line-item level).
- The transaction line - item  level grain was chosen to allow detail
analysis at the lowest level of sales data. This granularity enables precise reporting such as product-level performance, customer buying behavior, and time-based trends without losing detail.

2. Why surrogate keys instead of natural keys.
- Surrogate Keys are used instead of natural keys because they improve query performance and ensure stability in the data warehouse. Natural Key may change over time or vary across source system,Whereas surrogate keys remain consostent and support slowly changing dimensions.

3. How this design supports drill-down and roll-up operations.
- This Star Schema design supports both drill-down and roll-up operations. Analysts can drill down from yearly sales to quarterly, monthly, or daily views using the date dimension. Similarly, roll-up operations allow aggreation from product-level data to category-level insights, making the model highly flexible for analytical reporting.

-------------------------------------------------------------------------
#---------------------Section 3: Sample Data Flow-----------------------#

Source Transaction:
Order 101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000

Becomes in Data Warehouse:

fact_sales: {
  date_key: 20240115,
  product_key: 5,
  customer_key: 12,
  quantity_sold: 2,
  unit_price: 50000,
  total_amount: 100000
}

dim_date: {
  date_key: 20240115,
  full_date: '2024-01-15',
  month: 1,
  quarter: 'Q1',
  year: 2024
}

dim_product: {
     product_key: 5,
     product_name: 'Laptop',
     category: 'Electronics',
     brand: 'Lenovo',
     storage_capacity: 128GB SSDs,
     ram: 4GB to 64GB
}

dim_customer: {
     customer_key: 12,
     customer_name: 'John Doe',
     city: 'Mumbai',
     state:'Maharashtra',
     country:'India',
     customer_segnment: 'Corporate'
}
