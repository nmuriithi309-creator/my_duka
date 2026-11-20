# My Duka

A simple shop management app built with Flask and PostgreSQL. It lists products, records sales and tracks stock.

## Run it
1. Install the packages: `pip install flask psycopg2-binary`
2. Create a PostgreSQL database called `myduka` with `products`, `sales` and `stock` tables.
3. Copy `config_example.py` to `config.py` and put your PostgreSQL password in it.
4. Start the app: `python3 main.py`, then open http://127.0.0.1:5000
