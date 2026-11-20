from flask import Flask, render_template, request, redirect, url_for
from database import get_products, fetch_sales, insert_products
from database import fetch_sales, insert_sales
from database import fetch_stock, insert_stock


#flask instance
app = Flask(__name__)


@app.route('/') #decorator function
def home (): #view function
    return render_template('index.html')


@app.route('/products')
def products():
    products_data = get_products()
    return render_template ('products.html',products_data = products_data)

@app.route('/add_products', methods=['GET','POST'])
def add_products():
    if request.method =="POST":
        product_name = request.form['p_name']
        buying_price = request.form['b_price']
        selling_price = request.form['s_price']

        new_products = (product_name,buying_price,selling_price)
        insert_products(new_products)
        print("products added successfully")
    return redirect(url_for('products'))


@app.route('/sales')
def sales():
    sales_data = fetch_sales()
    products_data = get_products()
    return render_template ('sales.html',sales_data = sales_data, products_data = products_data)

@app.route('/add_sales', methods=['GET','POST'])
def add_sales():
    if request.method =="POST":
        product_id = request.form['pid']
        quantity = request.form['quantity']

        new_sale = (product_id,quantity)
        insert_sales(new_sale)
        print("sale added successfully")
    return redirect(url_for('sales'))


@app.route('/dashboard')
def dashboard():
    return render_template ('dashboard.html')

@app.route('/register')
def register():
    return render_template ('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/stock')
def stock():
    stock_data = fetch_stock()
    products_data = get_products()
    return render_template('stock.html',stock_data = stock_data, products_data = products_data)

@app.route('/add_stock', methods=['GET','POST'])
def add_stock():
    if request.method =="POST":
        product_id = request.form['pid']
        stock_quantity = request.form['stock_quantity']

        new_stock = (product_id,stock_quantity)
        insert_stock(new_stock)
        print("stock added successfully")
    return redirect(url_for('stock'))


#starts server to run app
if __name__ == '__main__':
    app.run(debug=True)