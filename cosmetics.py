import psycopg2

# establishing a db connection
conn = psycopg2.connect(host='localhost', port=5432, user='naomimuriithi', dbname='myduka')

# creating a cur object to perform db operations
cur = conn.cursor()


# ---------- PRODUCTS ----------

def get_products():
    cur.execute("select * from products")
    products_data = cur.fetchall()
    return products_data


# Reusable function: insert any product using parameters
# "returning id" gives back the new product's id, so we can use it for stock and sales
def insert_products(prod_details):
    cur.execute(
        "insert into products(name, buying_price, selling_price) values (%s, %s, %s) returning id",
        prod_details,
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    return new_id


# ---------- STOCK ----------

def get_stock():
    cur.execute("select * from stock")
    stock_data = cur.fetchall()
    return stock_data


# Reusable function: insert any stock using parameters
def insert_stock(stock_details):
    cur.execute("insert into stock(pid, stock_quantity) values (%s, %s)", stock_details)
    conn.commit()


# ---------- SALES ----------

def get_sales():
    cur.execute("select * from sales")
    sales_data = cur.fetchall()
    return sales_data


# Reusable function: insert any sale using parameters
def insert_sales(sales_details):
    cur.execute("insert into sales(pid, quantity) values (%s, %s)", sales_details)
    conn.commit()


# ---------- REPORTS ----------

def get_sales_per_product():
    cur.execute("""
        select products.name as p_name,
               sum(products.selling_price * sales.quantity) as total_sales
        from sales
        join products on products.id = sales.pid
        group by p_name
        order by total_sales desc;
    """)
    sales_per_product = cur.fetchall()
    return sales_per_product


def get_sales_per_day():
    cur.execute("""
        select date(sales.created_at) as sale_day,
               sum(products.selling_price * sales.quantity) as total_sales
        from sales
        join products on products.id = sales.pid
        group by sale_day
        order by sale_day;
    """)
    sales_per_day = cur.fetchall()
    return sales_per_day


def get_profit_per_product():
    cur.execute("""
        select products.name as p_name,
               sum((products.selling_price - products.buying_price) * sales.quantity) as total_profit
        from sales
        join products on products.id = sales.pid
        group by products.id, products.name
        order by total_profit desc;
    """)
    profit_per_product = cur.fetchall()
    return profit_per_product


def get_profit_per_day():
    cur.execute("""
        select date(sales.created_at) as sale_day,
               sum((products.selling_price - products.buying_price) * sales.quantity) as total_profit
        from sales
        join products on products.id = sales.pid
        group by sale_day
        order by sale_day;
    """)
    profit_per_day = cur.fetchall()
    return profit_per_day


# ---------- ADD COSMETICS DATA ----------
# Run this section ONCE, then put # in front of every line in it,
# otherwise the same products, stock and sales get added again on every run.

# (name, buying_price, selling_price) in KSh
lipstick = insert_products(('Matte lipstick', 350, 600))
foundation = insert_products(('Liquid foundation', 900, 1500))
mascara = insert_products(('Waterproof mascara', 450, 800))
lotion = insert_products(('Shea body lotion', 300, 550))
nail_polish = insert_products(('Nail polish', 120, 250))

# (product id, stock quantity)
insert_stock((lipstick, 60))
insert_stock((foundation, 25))
insert_stock((mascara, 40))
insert_stock((lotion, 50))
insert_stock((nail_polish, 80))

# (product id, quantity sold)
insert_sales((lipstick, 5))
insert_sales((foundation, 2))
insert_sales((mascara, 3))
insert_sales((lotion, 4))
insert_sales((nail_polish, 6))


# ---------- SHOW EVERYTHING ----------

print("Products:", get_products())
print("Stock:", get_stock())
print("Sales:", get_sales())
print("Sales per product:", get_sales_per_product())
print("Sales per day:", get_sales_per_day())
print("Profit per product:", get_profit_per_product())
print("Profit per day:", get_profit_per_day())
