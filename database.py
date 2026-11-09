import psycopg2


#establishing a db connection
conn = psycopg2.connect(host='localhost', port=5432, user='naomimuriithi', dbname='myduka')


#creating a cur object to perform db operations
cur = conn.cursor()


def get_product():
    cur.execute("select * from products")
    products_data = cur.fetchall()
    return products_data


def insert_products():
    cur.execute("insert into products(name,buying_price,selling_price)values('asus laptop',4000,5000)")
    conn.commit()


products_data = get_product()
print(products_data)
# insert_products()
insert_products()
products_data = get_product()
print(products_data)

#Fetch stock data (Task 1)
def get_stock():
    cur.execute("select * from stock")
    stock_data = cur.fetchall()
    return stock_data

#Insert any stock data with parameters (Task 2)
def insert_stock(values):
    query = "insert into stock(pid, stock_quantity) values (%s, %s)"
    cur.execute(query, values)
    conn.commit()
#Add some sales
def insert_sales(values):
    query = "insert into sales(pid, quantity) values (%s, %s)"
    cur.execute(query, values)
    conn.commit()

#Sales per day
def sales_per_day():
    query = """
        select date(sales.created_at) as day,
               sum(products.selling_price * sales.quantity) as total_sales
        from sales
        join products on sales.pid = products.id
        group by day
        order by day
    """
    cur.execute(query)
    return cur.fetchall()

#Profit per product
def profit_per_product():
    query = """
        select products.name,
               sum((products.selling_price - products.buying_price) * sales.quantity) as profit
        from sales
        join products on sales.pid = products.id
        group by products.name
    """
    cur.execute(query)
    return cur.fetchall()

#Profit per day
def profit_per_day():
    query = """
        select date(sales.created_at) as day,
               sum((products.selling_price - products.buying_price) * sales.quantity) as profit
        from sales
        join products on sales.pid = products.id
        group by day
        order by day
    """
    cur.execute(query)
    return cur.fetchall()

insert_sales((1, 2))
insert_sales((2, 3))
insert_sales((3, 1))

print("Stock:", get_stock())
print("Sales per day:", sales_per_day())
print("Profit per product:", profit_per_product())
print("Profit per day:", profit_per_day())