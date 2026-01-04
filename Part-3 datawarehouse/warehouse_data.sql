
USE fleximart_dw;

-----dim_date: 30 dates (January-February 2024)-----

INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,false),
(20240116,'2024-01-16','Tuesday',16,1,'January','Q1',2024,false),
(20240117,'2024-01-17','Wednesday',17,1,'January','Q1',2024,false),
(20240118,'2024-01-18','Thursday',18,1,'January','Q1',2024,false),
(20240119,'2024-01-19','Friday',19,1,'January','Q1',2024,false),
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,true),
(20240121,'2024-01-21','Sunday',21,1,'January','Q1',2024,true),
(20240122,'2024-01-22','Monday',22,1,'January','Q1',2024,false),
(20240123,'2024-01-23','Tuesday',23,1,'January','Q1',2024,false),
(20240124,'2024-01-24','Wednesday',24,1,'January','Q1',2024,false),
(20240125,'2024-01-25','Thursday',25,1,'January','Q1',2024,false),
(20240126,'2024-01-26','Friday',26,1,'January','Q1',2024,false),
(20240127,'2024-01-27','Saturday',27,1,'January','Q1',2024,true),
(20240128,'2024-01-28','Sunday',28,1,'January','Q1',2024,true),
(20240129,'2024-01-29','Monday',29,1,'January','Q1',2024,false),
(20240130,'2024-01-30','Tuesday',30,1,'January','Q1',2024,false),
(20240131,'2024-01-31','Wednesday',31,1,'January','Q1',2024,false),
(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,false),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,false),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,true),

(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,true),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,false),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,false),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,false),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,false),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,false),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,true),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,true),
(20240212,'2024-02-12','Monday',12,2,'February','Q1',2024,false),
(20240213,'2024-02-13','Tuesday',13,2,'February','Q1',2024,false);


----- dim_product: 15 products across 3 categories------

INSERT INTO dim_product (product_key, product_id, product_name, category, subcategory, unit_price) VALUES
(1,'ELEC001','Samsung Galaxy S21 Ultra','Electronics','Smartphones',79999.00),
(2,'ELEC002','Lenovo IdeaPad Slim 5','Electronics','Laptops',64999.00),
(3,'ELEC003','Sony WH-1000XM5','Electronics','Headphones',24999.00),
(4,'ELEC004','Mi Smart TV 43','Electronics','Television',29999.00),
(5,'ELEC005','Logitech Wireless Mouse','Electronics','Accessories',999.00),

(6,'HOME001','Prestige Induction Cooktop','Home & Kitchen','Appliances',2799.00),
(7,'HOME002','Milton Thermosteel Bottle','Home & Kitchen','Kitchenware',699.00),
(8,'HOME003','Philips Mixer Grinder','Home & Kitchen','Appliances',3499.00),
(9,'HOME004','Wakefit Queen Mattress','Home & Kitchen','Furniture',12999.00),
(10,'HOME005','IKEA Study Table','Home & Kitchen','Furniture',8999.00),

(11,'FASH001','Men Cotton T-Shirt','Fashion','Clothing',399.00),
(12,'FASH002','Women Kurti','Fashion','Clothing',899.00),
(13,'FASH003','Running Shoes','Fashion','Footwear',2499.00),
(14,'FASH004','Leather Wallet','Fashion','Accessories',799.00),
(15,'FASH005','Smart Watch Band','Fashion','Accessories',299.00);

-----dim_customer: 12 customers across 4 cities----

INSERT INTO dim_customer (customer_key, customer_id, customer_name, city, state, customer_segment) VALUES
(1,'CUST001','Aarav Mehta','Mumbai','Maharashtra','Consumer'),
(2,'CUST002','Isha Sharma','Pune','Maharashtra','Consumer'),
(3,'CUST003','Rahul Verma','Bengaluru','Karnataka','Consumer'),
(4,'CUST004','Neha Singh','Delhi','Delhi','Consumer'),
(5,'CUST005','Kunal Patil','Mumbai','Maharashtra','Corporate'),
(6,'CUST006','Sneha Kulkarni','Pune','Maharashtra','SmallBiz'),
(7,'CUST007','Vikram Rao','Bengaluru','Karnataka','Corporate'),
(8,'CUST008','Ananya Gupta','Delhi','Delhi','SmallBiz'),
(9,'CUST009','Rohan Joshi','Mumbai','Maharashtra','Consumer'),
(10,'CUST010','Priya Nair','Bengaluru','Karnataka','Consumer'),
(11,'CUST011','Siddharth Jain','Delhi','Delhi','Corporate'),
(12,'CUST012','Meera Deshmukh','Pune','Maharashtra','Consumer');

-----fact_sales: 40 sales transactions-----

INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
(20240115,2,1,1,64999.00,1500.00,63499.00),
(20240116,5,2,2,999.00,0.00,1998.00),
(20240117,7,3,3,699.00,50.00,2047.00),
(20240118,11,4,2,399.00,0.00,798.00),
(20240119,3,5,1,24999.00,1000.00,23999.00),

(20240120,1,1,2,79999.00,2500.00,157498.00),
(20240120,13,6,3,2499.00,200.00,7297.00),
(20240121,9,7,1,12999.00,500.00,12499.00),
(20240121,6,8,2,2799.00,0.00,5598.00),

(20240122,4,9,1,29999.00,1200.00,28799.00),
(20240123,12,10,2,899.00,100.00,1698.00),
(20240124,8,11,1,3499.00,0.00,3499.00),
(20240125,14,12,2,799.00,0.00,1598.00),
(20240126,10,2,1,8999.00,300.00,8699.00),

(20240127,2,3,2,64999.00,2000.00,127998.00),
(20240127,11,4,4,399.00,0.00,1596.00),
(20240128,3,5,2,24999.00,1500.00,48498.00),
(20240128,7,6,5,699.00,0.00,3495.00),
(20240129,15,7,3,299.00,0.00,897.00),
(20240130,5,8,1,999.00,0.00,999.00),
(20240131,6,9,1,2799.00,100.00,2699.00),

(20240201,13,10,1,2499.00,0.00,2499.00),
(20240202,12,11,3,899.00,150.00,2547.00),
(20240203,4,12,2,29999.00,2000.00,57998.00),
(20240203,9,1,2,12999.00,500.00,25498.00),
(20240204,1,2,1,79999.00,3000.00,76999.00),
(20240204,10,3,2,8999.00,0.00,17998.00),

(20240205,8,4,1,3499.00,0.00,3499.00),
(20240206,7,5,2,699.00,0.00,1398.00),
(20240207,11,6,3,399.00,0.00,1197.00),
(20240208,14,7,1,799.00,0.00,799.00),
(20240209,3,8,1,24999.00,500.00,24499.00),

(20240210,2,9,1,64999.00,2000.00,62999.00),
(20240210,6,10,3,2799.00,200.00,8197.00),
(20240211,13,11,2,2499.00,0.00,4998.00),
(20240211,4,12,1,29999.00,1000.00,28999.00),

(20240212,5,1,3,999.00,0.00,2997.00),
(20240212,12,2,1,899.00,0.00,899.00),
(20240213,7,3,2,699.00,0.00,1398.00),
(20240213,9,4,1,12999.00,0.00,12999.00);
