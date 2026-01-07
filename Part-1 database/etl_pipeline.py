from dotenv import load_dotenv
import os
import re
from datetime import datetime

import pandas as pd
import mysql.connector

load_dotenv()

# ----------------------------
# CONFIG
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),
    "database": "fleximart",
}

DATA_DIR = "data"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DATA_DIR = os.path.join(BASE_DIR, "data")

CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers_raw.csv")
PRODUCTS_FILE  = os.path.join(DATA_DIR, "products_raw.csv")
SALES_FILE     = os.path.join(DATA_DIR, "sales_raw.csv")
REPORT_FILE = "data_quality_report.txt"

# ----------------------------
# HELPERS (TRANSFORM)
# ----------------------------
def clean_phone(x):
    if pd.isna(x):
        return None
    x = re.sub(r"[^\d]", "", str(x))  # keep digits only
    if x.startswith("91") and len(x) > 10:
        x = x[2:]
    if x.startswith("0") and len(x) > 10:
        x = x[1:]
    return x if len(x) == 10 else None


def parse_date(x):
    if pd.isna(x):
        return None

    x = str(x).strip()

    # Try known formats first
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(x, fmt).date()
        except ValueError:
            pass

    # Fallback: pandas parser
    try:
        return pd.to_datetime(x, errors="coerce").date()
    except Exception:
        return None


def normalize_category(x):
    if pd.isna(x):
        return None
    x = str(x).strip().lower()
    mapping = {
        "electronics": "Electronics",
        "fashion": "Fashion",
        "groceries": "Groceries",
    }
    return mapping.get(x, x.title())

# ----------------------------
# LOAD HELPERS (MYSQL)
# ----------------------------
def insert_many(cursor, sql, rows):
    if not rows:
        return 0
    cursor.executemany(sql, rows)
    return cursor.rowcount


def main():
    counts = {
        "customers_raw": 0,
        "products_raw": 0,
        "sales_raw": 0,
        "customers_loaded": 0,
        "products_loaded": 0,
        "orders_loaded": 0,
        "order_items_loaded": 0,
        "customers_dupes_removed": 0,
        "sales_dupes_removed": 0,
        "missing_emails_handled": 0,
        "missing_prices_handled": 0,
        "missing_stock_handled": 0,
        "sales_missing_customer_removed": 0,
        "sales_missing_product_removed": 0,
    }

    conn = None
    cursor = None

    try:
        # ----------------------------
        # CONNECT
        # ----------------------------
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        print("Connected to database:", cursor.fetchone())

        # ----------------------------
        # EXTRACT
        # ----------------------------
        customers_df = pd.read_csv(CUSTOMERS_FILE)
        products_df = pd.read_csv(PRODUCTS_FILE)
        sales_df = pd.read_csv(SALES_FILE)

        counts["customers_raw"] = len(customers_df)
        counts["products_raw"] = len(products_df)
        counts["sales_raw"] = len(sales_df)

        print("\n--- EXTRACT ---")
        print("Customers rows (raw):", counts["customers_raw"])
        print("Products rows (raw):", counts["products_raw"])
        print("Sales rows (raw):", counts["sales_raw"])

        # ----------------------------
        # TRANSFORM: CUSTOMERS
        # ----------------------------
        print("\n--- TRANSFORM: CUSTOMERS ---")
        customers_df = customers_df.dropna(how="all")

        # trim + title case
        customers_df["customer_id"] = customers_df["customer_id"].astype(str).str.strip()
        customers_df["first_name"] = customers_df["first_name"].astype(str).str.strip().str.title()
        customers_df["last_name"] = customers_df["last_name"].astype(str).str.strip().str.title()
        customers_df["city"] = customers_df["city"].astype(str).str.strip().str.title()

        # phone normalize
        customers_df["phone"] = customers_df["phone"].apply(clean_phone)

        # missing emails -> generate placeholder
        missing_email_mask = customers_df["email"].isna()
        counts["missing_emails_handled"] = int(missing_email_mask.sum())
        customers_df.loc[missing_email_mask, "email"] = (
            customers_df.loc[missing_email_mask, "customer_id"].str.lower() + "@missing.com"
        )

        # date normalize
        customers_df["registration_date"] = customers_df["registration_date"].apply(parse_date)

        # remove duplicate customer_id
        before = len(customers_df)
        customers_df = customers_df.drop_duplicates(subset=["customer_id"], keep="first")
        counts["customers_dupes_removed"] = before - len(customers_df)

        print("Missing emails handled:", counts["missing_emails_handled"])
        print("Customer duplicates removed:", counts["customers_dupes_removed"])

        # ----------------------------
        # TRANSFORM: PRODUCTS
        # ----------------------------
        print("\n--- TRANSFORM: PRODUCTS ---")
        products_df = products_df.dropna(how="all")

        products_df["product_id"] = products_df["product_id"].astype(str).str.strip()
        products_df["product_name"] = products_df["product_name"].astype(str).str.strip()
        products_df["category"] = products_df["category"].apply(normalize_category)

        # stock: missing -> 0
        missing_stock_mask = products_df["stock_quantity"].isna()
        counts["missing_stock_handled"] = int(missing_stock_mask.sum())
        products_df.loc[missing_stock_mask, "stock_quantity"] = 0

        products_df["stock_quantity"] = products_df["stock_quantity"].astype(int)

        # price: missing -> use median price of that category (fallback overall median)
        missing_price_mask = products_df["price"].isna()
        counts["missing_prices_handled"] = int(missing_price_mask.sum())

        # convert to numeric
        products_df["price"] = pd.to_numeric(products_df["price"], errors="coerce")

        overall_median = products_df["price"].median()
        for cat in products_df["category"].dropna().unique():
            cat_mask = products_df["category"] == cat
            cat_median = products_df.loc[cat_mask, "price"].median()
            if pd.isna(cat_median):
                cat_median = overall_median
            products_df.loc[cat_mask & products_df["price"].isna(), "price"] = cat_median

        # if still NA, fill with overall median
        products_df["price"] = products_df["price"].fillna(overall_median)

        print("Missing stock handled:", counts["missing_stock_handled"])
        print("Missing prices handled:", counts["missing_prices_handled"])

        # ----------------------------
        # TRANSFORM: SALES
        # ----------------------------
        print("\n--- TRANSFORM: SALES ---")
        sales_df = sales_df.dropna(how="all")

        sales_df["transaction_id"] = sales_df["transaction_id"].astype(str).str.strip()
        sales_df["customer_id"] = sales_df["customer_id"].astype(str).str.strip()
        sales_df["product_id"] = sales_df["product_id"].astype(str).str.strip()

        # fix "nan" strings back to NaN
        sales_df.loc[sales_df["customer_id"].str.lower() == "nan", "customer_id"] = pd.NA
        sales_df.loc[sales_df["product_id"].str.lower() == "nan", "product_id"] = pd.NA

        # date normalize
        sales_df["transaction_date"] = sales_df["transaction_date"].apply(parse_date)

        # remove duplicate transaction_id
        before = len(sales_df)
        sales_df = sales_df.drop_duplicates(subset=["transaction_id"], keep="first")
        counts["sales_dupes_removed"] = before - len(sales_df)

        # remove rows missing customer_id or product_id
        missing_customer_mask = sales_df["customer_id"].isna()
        missing_product_mask = sales_df["product_id"].isna()
        counts["sales_missing_customer_removed"] = int(missing_customer_mask.sum())
        counts["sales_missing_product_removed"] = int(missing_product_mask.sum())

        sales_df = sales_df[~missing_customer_mask]
        sales_df = sales_df[~missing_product_mask]

        print("Sales duplicates removed:", counts["sales_dupes_removed"])
        print("Missing customer_id removed rows:", counts["sales_missing_customer_removed"])
        print("Missing product_id removed rows:", counts["sales_missing_product_removed"])

        # ----------------------------
        # LOAD
        # ----------------------------
        print("\n--- LOAD ---")

        # 1) Load customers (use customer_id from CSV)
        customers_rows = [
            (
                r["customer_id"],
                r["first_name"],
                r["last_name"],
                r["email"],
                r["phone"],
                r["city"],
                r["registration_date"],
            )
            for _, r in customers_df.iterrows()
        ]

        sql_customers = """
            INSERT INTO customers (customer_id, first_name, last_name, email, phone, city, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                first_name=VALUES(first_name),
                last_name=VALUES(last_name),
                email=VALUES(email),
                phone=VALUES(phone),
                city=VALUES(city),
                registration_date=VALUES(registration_date);
        """
        counts["customers_loaded"] = insert_many(cursor, sql_customers, customers_rows)
        conn.commit()

        # 2) Load products
        products_rows = [
            (
                r["product_id"],
                r["product_name"],
                r["category"],
                float(r["price"]),
                int(r["stock_quantity"]),
            )
            for _, r in products_df.iterrows()
        ]

        sql_products = """
            INSERT INTO products (product_id, product_name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                product_name=VALUES(product_name),
                category=VALUES(category),
                price=VALUES(price),
                stock_quantity=VALUES(stock_quantity);
        """
        counts["products_loaded"] = insert_many(cursor, sql_products, products_rows)
        conn.commit()

        # 3) Create orders + order_items from sales
        #    order = 1 transaction
        #    order_item = that transaction line
        orders_rows = []
        items_rows = []

        for _, r in sales_df.iterrows():
            qty = int(r["quantity"])
            unit_price = float(r["unit_price"])
            total = qty * unit_price
            orders_rows.append(
                (r["transaction_id"], r["customer_id"], r["transaction_date"], total, r["status"])
            )

        sql_orders = """
            INSERT INTO orders (transaction_id, customer_id, order_date, total_amount, status)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                customer_id=VALUES(customer_id),
                order_date=VALUES(order_date),
                total_amount=VALUES(total_amount),
                status=VALUES(status);
        """
        counts["orders_loaded"] = insert_many(cursor, sql_orders, orders_rows)
        conn.commit()

        # Fetch order_id for each transaction_id
        cursor.execute("SELECT order_id, transaction_id FROM orders;")
        order_map = {tx: oid for (oid, tx) in cursor.fetchall()}

        for _, r in sales_df.iterrows():
            oid = order_map.get(r["transaction_id"])
            if not oid:
                continue
            qty = int(r["quantity"])
            unit_price = float(r["unit_price"])
            subtotal = qty * unit_price
            items_rows.append((oid, r["product_id"], qty, unit_price, subtotal))

        sql_items = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s);
        """
        counts["order_items_loaded"] = insert_many(cursor, sql_items, items_rows)
        conn.commit()

        print("Loaded customers:", counts["customers_loaded"])
        print("Loaded products:", counts["products_loaded"])
        print("Loaded orders:", counts["orders_loaded"])
        print("Loaded order_items:", counts["order_items_loaded"])

        # ----------------------------
        # REPORT FILE
        # ----------------------------
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("FlexiMart ETL - Data Quality Report\n")
            f.write("=" * 40 + "\n\n")

            f.write("Records processed:\n")
            f.write(f"- customers_raw.csv: {counts['customers_raw']}\n")
            f.write(f"- products_raw.csv: {counts['products_raw']}\n")
            f.write(f"- sales_raw.csv: {counts['sales_raw']}\n\n")

            f.write("Duplicates removed:\n")
            f.write(f"- customers duplicates removed: {counts['customers_dupes_removed']}\n")
            f.write(f"- sales duplicates removed: {counts['sales_dupes_removed']}\n\n")

            f.write("Missing values handled:\n")
            f.write(f"- missing emails handled: {counts['missing_emails_handled']}\n")
            f.write(f"- missing prices handled: {counts['missing_prices_handled']}\n")
            f.write(f"- missing stock handled: {counts['missing_stock_handled']}\n")
            f.write(f"- sales rows removed (missing customer_id): {counts['sales_missing_customer_removed']}\n")
            f.write(f"- sales rows removed (missing product_id): {counts['sales_missing_product_removed']}\n\n")

            f.write("Records loaded successfully:\n")
            f.write(f"- customers loaded/updated: {counts['customers_loaded']}\n")
            f.write(f"- products loaded/updated: {counts['products_loaded']}\n")
            f.write(f"- orders loaded/updated: {counts['orders_loaded']}\n")
            f.write(f"- order_items loaded: {counts['order_items_loaded']}\n")

        print(f"\n Report generated: {REPORT_FILE}")
        print(" ETL completed successfully!")

    except Exception as e:
        print(" ETL failed:", e)

    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            print("Connection closed")
        except Exception:
            pass


if __name__ == "__main__":
    main()
