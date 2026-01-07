

SELECT database()

USE fleximart_dw;

select 1;

#---- Query 1: Monthly Sales Drill-Down Analysis ----#
select
  d.year,
  d.quarter,
  d.month_name,
  SUM(f.total_amount) as total_sales,
  SUM(f.quantity_sold) as total_quantity
from fact_sales f
join dim_date d ON f.date_key = d.date_key
where d.year = 2024
GROUP BY d.year, d.quarter, d.month, d.month_name
ORDER BY d.year, d.quarter, d.month;
 

#---- Query 2: Product Performance Analysis ----#

SELECT
  t.product_name,
  t.category,
  t.units_sold,
  t.revenue,
  ROUND((t.revenue / totals.total_revenue) * 100, 2) AS revenue_percentage
FROM (
  SELECT
    p.product_name,
    p.category,
    SUM(f.quantity_sold) AS units_sold,
    SUM(f.total_amount) AS revenue
  FROM fact_sales f
  JOIN dim_product p ON f.product_key = p.product_key
  GROUP BY p.product_key, p.product_name, p.category
) t
CROSS JOIN (
  SELECT SUM(total_amount) AS total_revenue FROM fact_sales
) totals
ORDER BY t.revenue DESC
LIMIT 10;


#---- Query 3: Customer Segmentation Analysis ----#

WITH customer_spend AS (
  SELECT
    c.customer_key,
    c.customer_name,
    SUM(f.total_amount) AS total_spend
  FROM fact_sales f
  JOIN dim_customer c ON f.customer_key = c.customer_key
  GROUP BY c.customer_key, c.customer_name
),
segmented AS (
  SELECT
    CASE
      WHEN total_spend > 50000 THEN 'High Value'
      WHEN total_spend BETWEEN 20000 AND 50000 THEN 'Medium Value'
      ELSE 'Low Value'
    END AS customer_segment,
    total_spend
  FROM customer_spend
)
SELECT
  customer_segment,
  COUNT(*) AS customer_count,
  SUM(total_spend) AS total_revenue,
  ROUND(AVG(total_spend), 2) AS avg_revenue_per_customer
FROM segmented
GROUP BY customer_segment
ORDER BY total_revenue DESC;

