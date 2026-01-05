# FlexiMart Data Architecture Project

**Student Name :** Harshada Nawade  
**Student ID :**   2507677  
**Program :**      BITSOM – Business Analytics  
**Repository :**   bitsom_ba_2507677_FlexiMart-Data-Architecture  
**Date :**         January 2026  

# Project Overview

This project implements an end-to-end data architecture solution for FlexiMart, covering transactional data processing, NoSQL catalog modeling, and analytical reporting. The solution includes a relational database with ETL, a MongoDB-based product catalog, and a data warehouse designed using a star schema to support business analytics and decision-making.

## Repository Structure

├── data/
│ ├── customers_raw.csv
│ ├── products_raw.csv
│ └── sales_raw.csv
│
├── part1-database-etl/
│ ├── etl_pipeline.py
│ ├── schema_documentation.md
│ ├── business_queries.sql
│ └── data_quality_report.txt
│
├── part2-nosql/
│ ├── nosql_analysis.md
│ ├── mongodb_operations.js
│ └── products_catalog.json
│
├── part3-datawarehouse/
│ ├── star_schema_design.md
│ ├── warehouse_schema.sql
│ ├── warehouse_data.sql
│ └── analytics_queries.sql
│
└── README.md

## Technologies Used

**Programming:**         Python 3.x  
**Libraries:**           pandas, mysql-connector-python  
**Relational Database:** MySQL 8.0 / PostgreSQL  
**NoSQL Database:**      MongoDB 6.0  
**Data Modeling:**       Star Schema (Fact & Dimension tables)  


# Run Part 1 - ETL Pipeline

**Description :**
This part focuses on ingesting raw transactional data and transforming it into a structured relational schema. The ETL pipeline handles data cleansing, type validation, and loading into normalized tables.

**How to Run :**
```bash

# Create transactional database 
mysql -u root -p -e "CREATE DATABASE fleximart;"

# Run ETL pipeline
py etl_pipeline.py

# Execute business queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Data Quality Checks: Documented in data_quality_report.txt, including:

- Null value validation for critical fields
- Primary key uniqueness checks
- Referential integrity validation
- Invalid value and range checks
---------------------------------------------------------------------------------------------

# Run Part 2 - NoSQL (MongoDB)

 **Description:**  MongoDB is used to model a flexible product catalog, where product attributes vary by category. This structure avoids frequent  schema changes and supports nested product attributes efficiently.
 
 **How_to_Run:** Part-2 nosql> node mongodb_operations.js

 **Contents:** 
 - Product catalog JSON
 - CRUD operations
 - Index creation
 - Query examples
 - Rationale for choosing NoSQL over relational modeling


-------------------------------------------------------------------------------------------------

 # Part 3 - Data Warehouse & Analytics

 **Description:** A star schema data warehouse is implemented to support analytical queries and reporting.

 **Schema_Design:**
 - Fact Table: Sales facts (quantity, revenue, discounts)
 - Dimension Tables: Date, Customer, Product

 **How_to_Run:**

 # Create data warehouse database
 mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

 # Create schema
 mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql

 # Load warehouse data
 mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql

 # Run analytics queries
 mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql  

 
## Key Learnings :
 - Designing ETL pipeline that balance data quality with performance.
 - Choosing between SQL and NoSql based on data structure and access patterns.
 - Implementing star schemas for analtical workloads.
 - Applying data validation techniques to ensure reliable reporting.

 ## Challenges Faced :
  - Handling inconsistent raw data formats
    Solution: Applied validation rules and transformations during ETL.

  - Modeling flexible product attributes
    Solution: Used MongoDB with nested documents instead of rigid relational schemas.



