# Std lib imports
from collections import defaultdict

# Flask imports
from flask import Blueprint, render_template, request

# Internal module imports
from inventory_manager.db import get_db

# Create a blueprint
bp = Blueprint('report', __name__)

# ------------------
# HELPER FUNCTIONS
# ------------------
def get_product_movements():
    '''return a list of all product movement records'''
    db = get_db()
    select_sql_query = 'SELECT * FROM ProductMovement ORDER BY product_id'
    prod_moves = db.execute(select_sql_query).fetchall()
    return prod_moves

# ----------
# ROUTES
# ----------
# render a page with a report
@bp.route('/', methods=("GET",))
def index():
    # Get productMovement records from database
    product_moves = get_product_movements()

    # To store stock data
    inventory = defaultdict(dict)

    for product_move in product_moves:
        # Extract product information
        product_id = product_move['product_id']
        to_location = product_move['to_location']
        from_location = product_move['from_location']
        qty = product_move['qty']

        # If only to_location is present
        if from_location is None:
            if to_location in inventory[product_id]:
                inventory[product_id][to_location] += qty
            else:
                inventory[product_id][to_location] = qty
        
        # If only from_location is present
        elif to_location is None:
            if from_location in inventory[product_id]:
                inventory[product_id][from_location] -= qty
            else:
                inventory[product_id][from_location] = -qty

        # Both locations are present
        else:
            # Increase the qty at the location
            # to where the product is moved
            inventory[product_id][to_location] = inventory[product_id].get(
                                                    to_location,
                                                    0
                                                ) + qty
                                                
            # Decrease the qty at the location
            # from where the product is moved
            inventory[product_id][from_location] = inventory[product_id].get(
                                                    from_location,
                                                    0
                                                ) - qty


    # render report with inventory data
    return render_template(
        'reports/inventory_report.html', 
        inventory=inventory
    )