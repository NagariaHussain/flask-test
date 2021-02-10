from flask import Blueprint, request, render_template, flash, redirect, abort
from flask.helpers import url_for
from inventory_manager.db import get_db

# Blueprint for '/product' endpoint
bp = Blueprint('product', __name__, url_prefix='/product')

def get_all_products():
    '''return a list of all the records in the `Product` table'''
    db = get_db()
    sql_query = 'SELECT * FROM Product'
    products = db.execute(sql_query).fetchall()
    return products

def get_product(product_id: str):
    '''return a single product record with the given `product_id`,
       abort with 404, if not found'''
    # Get database connection instance
    db = get_db()
    select_sql_query = 'SELECT * FROM Product WHERE product_id = ?'
    product = db.execute(select_sql_query, (product_id,)).fetchone()

    # If product is not found
    if product is None:
        abort(404, "Product Not Found!")

    return product

@bp.route('/', methods=('GET',))
def list_products():
    products = get_all_products()
    # Render a page containing all products
    return render_template('product/list.html', products=products)

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == "POST":
        error_message = None
        # Add the product to database
        product_id = request.form['product_id']

        if not product_id:
            error_message = 'product_id is required!'
        
        if error_message is not None:
            flash(error_message)
        else:
            db = get_db()
            insert_sql_query = 'INSERT INTO Product VALUES(?)'
            db.execute(insert_sql_query, (product_id,))
            db.commit()
            return redirect(url_for('product.list_products'))
        
    # Render product addition form
    return render_template('product/add.html')
        
@bp.route('/view/<product_id>', methods=("GET",))
def view(product_id: str):
    product = get_product(product_id)

    # Render the details of the product
    return render_template('product/details.html', product=product)

@bp.route('/edit/<product_id>', methods=("GET", "POST"))
def edit(product_id: str):
    product = get_product(product_id)
    
    if request.method == "POST":
        new_product_id = request.form['product_id']

        if not new_product_id:
            flash('Please provide a product id!')

        update_sql_query = "UPDATE Product SET product_id = ? WHERE product_id = ?"
        db = get_db()
        db.execute(update_sql_query, (new_product_id, product_id))
        db.commit()

        return redirect(url_for('product.list_products'))

    # Render a pre populated form 
    # with product data
    return render_template('product/edit.html', product=product)
