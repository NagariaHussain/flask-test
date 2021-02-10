from collections import defaultdict
from flask import Blueprint, render_template, request
from inventory_manager.db import get_db

bp = Blueprint('report', __name__)

def get_product_movements():
    '''return a list of all product movement records'''
    db = get_db()
    select_sql_query = 'SELECT * FROM ProductMovement'
    prod_moves = db.execute(select_sql_query).fetchall()
    return prod_moves

# Home page with a report
@bp.route('/', methods=("GET",))
def index():
    product_moves = get_product_movements()
    inventory = defaultdict(dict)

    for product_move in product_moves:
        product_id = product_move['product_id']
        to_location = product_move['to_location']
        from_location = product_move['from_location']
        qty = product_move['qty']

        if from_location is None:
            if to_location in inventory[product_id]:
                inventory[product_id][to_location] += qty
            else:
                inventory[product_id][to_location] = qty
        
        elif to_location is None:
            if from_location in inventory[product_id]:
                inventory[product_id][from_location] -= qty
            else:
                inventory[product_id][from_location] = -qty
        else:
            inventory[product_id][to_location] = inventory[product_id].get(
                                                    to_location,
                                                    0
                                                ) + qty
            inventory[product_id][from_location] = inventory[product_id].get(
                                                    from_location,
                                                    0
                                                ) - qty

    return render_template('reports/inventory_report.html', inventory=inventory)