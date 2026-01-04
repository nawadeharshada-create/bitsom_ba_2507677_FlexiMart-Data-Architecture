#------------------------Task 2.1: NoSQL Justification Report ---------------------------#

#------- Section A: Limitations of RDBMS -------#

Explain why the current relational database would struggle with:-
Relational databases like MySql work well when data is structured and consistent, but they face 
problems when product data becomes highly diverse. In FlexiMart, different products have different attributes. 
For Example:-Laptops need RAM and processor details, while shoes need size and color.
In RDBMS, this would require many optional columns or multiple tables, making the schema complex and inefficient.

Another issue is frequent schema changes:-
Whenever a new product type is added, the table structure must be altered using ALTER TABLE, which can be risky 
and slow for large databases. 
This reduces flexibility and increases maintenance effort.

Storing Customer review is also difficult in RDBMS. 
Reviews are naturally nested data(multiple review per product),but relational database require seperate tables
and joins, which increases query complexity and reduces performance.
Because of these reasons, a traditional ralational database struggles to scales to scale and adapt to 
FlexiMart's growing and changing product catalog.


#-------- Section B: NoSQL Benefits --------#

MongoDB solves these problems using a flexible, document-based data model.
Each product is stored as JSON-like document, allowing different products to have different attributes without changing the schema.
For Example:-A laptop document can store RAM and processor details, while a shoe document can store size and color. This flexibility makes 
MongoDB ideal for diverse product catalogs.

MongoDB also supports embedded documents, which allows customer reviews to be stored directly insided the product document. This reduces the need for joins and make data retrieval faster and simpler.

Another major advantage is horizontal scalability.
MongoDB can easily scale across multiple servers using sharding, which helps handle large volumes of data and high traffic.
This makes it suitable for growing applications like FlexiMart, where product data and user activity are expected to increase rapidly.


#--------- Section C: Trade-offs ----------#

What are two disadvantages of using MongoDB instead of MySQL for this product catalog?
One disadvantage of MongoDB is weaker support for complex transactions compared to MySQL. While MongoDB supports transactions, they can be more expensive and less efficient for highly relational data.

Another drawback is the lack of strict schema enforcement.Since MongoDB is schema - flexible, poor design can lead to inconsistent data if proper validation rules are not applied.
This shifts more responsibility to the application layer to maintain data qualoity.


#--- Conclusion ---#

 MongoDb is good choice for FleciMart's diverse and evolving product catalog because of its flexible schema, support for nested data, and scalability, even though it has some trade-offs compared to traditional relational databases.

