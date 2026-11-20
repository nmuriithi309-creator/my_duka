import psycopg2
from config import DB_PASSWORD

# establishing a db connection
conn = psycopg2.connect(host='localhost',port=5432, user='postgres',password=DB_PASSWORD,dbname='myduka')

# creating a cur object to perform db operations
cur = conn.cursor()


def get_products():
    cur.execute("select * from products")
    products_data = cur.fetchall()
    return products_data


def insert_products(prod_details):
    cur.execute("insert into products(name,buying_price,selling_price)values(%s,%s,%s)",prod_details) 
    conn.commit()





def fetch_sales():
    cur.execute(
    """
        select sales.id, products.name, sales.quantity, sales.created_at
        from sales join products on products.id = sales.pid;
    """)
    sales_data = cur.fetchall()
    return sales_data


def insert_sales(sale_details):
    cur.execute("insert into sales(pid,quantity)values(%s,%s)",sale_details)
    conn.commit()


def insert_stock(stock_details):
    cur.execute("insert into stock(pid,stock_quantity)values(%s,%s)",stock_details)
    conn.commit()


def fetch_stock():
    cur.execute(
    """
        select stock.id, products.name, stock.stock_quantity, stock.created_at
        from stock join products on products.id = stock.pid;
    """)
    stock_data = cur.fetchall()
    return stock_data


# sale1 = (2,45)
# sale2 = (1,10)
# insert_sales(sale1)
# insert_sales(sale2)

# sales_data = fetch_sales()
# print(sales_data)



def get_sales_per_product():
    cur.execute(
    """
        select products.name as p_name,sum(products.selling_price * sales.quantity) as total_sales
        from sales join products on products.id = sales.pid group by p_name;
    """)
    sales_per_product = cur.fetchall()
    return sales_per_product


sales_per_product = get_sales_per_product()
print(sales_per_product)



def get_sales_per_day():
    cur.execute(
    """
        select date(sales.created_at) as day,sum(products.selling_price * sales.quantity) as total_sales
        from sales join products on products.id = sales.pid group by day;
    """)
    sales_per_day = cur.fetchall()
    return sales_per_day



def get_profit_per_product():
    cur.execute(
    """
        select products.name as p_name,sum((products.selling_price - products.buying_price) * sales.quantity)
          as t_profit from sales join products on products.id = sales.pid group by p_name;
    """)
    profit_per_product = cur.fetchall()
    return profit_per_product


def get_profit_per_day():
    cur.execute(
    """
        select date(sales.created_at) as day,sum((products.selling_price - products.buying_price) * sales.quantity)
          as t_profit from sales join products on products.id = sales.pid group by day;
    """)
    profit_per_day = cur.fetchall()
    return profit_per_day
