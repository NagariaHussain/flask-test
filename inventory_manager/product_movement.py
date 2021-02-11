# Std lib imports
from datetime import datetime
from sqlite3.dbapi2 import Timestamp

# Flask imports
from flask import Blueprint, request, render_template, flash, redirect, abort
from flask.helpers import url_for

# Internal module imports
from inventory_manager.db import get_db
from inventory_manager.product import get_all_products
from inventory_manager.location import get_all_locations

# Blueprint for '/movement' endpoint
bp = Blueprint('movement', __name__, url_prefix='/movement')

def get_movement(movement_id: str):
    '''return a single movement record with the given `movement_id`,
       abort with 404, if not found'''
    # Get database connection instance
    db = get_db()
    select_sql_query = 'SELECT * FROM ProductMovement WHERE movement_id = ?'
    movement = db.execute(select_sql_query, (movement_id,)).fetchone()

    # If movement is not found
    if movement is None:
        abort(404, "Movement Not Found!")

    return movement

def get_timestamp(date: str, time: str):
    '''return python datetime object based on 
       given date and time strings'''
    timestamp = None
    # If time is not provided
    if time == "":
        time = datetime.now().strftime("%H:%M")

    # If date is not provided
    if date == "":
        date = datetime.now().strftime("%Y-%m-%d")
        
    # Create datetime object
    timestamp = datetime.strptime(
        f"{date}, {time}", 
        "%Y-%m-%d, %H:%M"
    )

    return timestamp

def process_and_save_movement(data, type, movement_id=None):
    # Extract query params
    product_id = data.get('product_id')
    from_location = data.get('from_location')
    to_location = data.get('to_location')
    qty = int(data.get('qty'))
    time = data.get('time')
    date = data.get('date')

    # Generate timestamp
    timestamp = get_timestamp(date, time)

    # Both the locations are unknown
    if from_location == "unknown" and to_location == "unknown":
        abort(400, "Both from and to locations cannot be none at the same time")
    # Source location is unknown
    elif from_location == "unknown":
        from_location = None
    # Destination location is unknown
    elif to_location == "unknown":
        to_location = None

    # Create new movement entry
    db = get_db()
    sql_query = None

    if type == "INSERT":
        sql_query = 'INSERT INTO ProductMovement(product_id, from_location, to_location, qty, timestamp) VALUES (?, ?, ?, ?, ?)'
        db.execute(
            sql_query,
            (product_id, from_location, to_location, qty, timestamp)
        )
    else:
        sql_query = 'UPDATE ProductMovement SET product_id = ?, from_location = ?, to_location = ?, qty = ?, timestamp = ? WHERE movement_id = ?'
        db.execute(
            sql_query,
            (product_id, from_location, to_location, qty, timestamp, movement_id)
        )

    # Commit to database
    db.commit()


@bp.route('/', methods=("GET",))
def index():
    db = get_db()
    movements = db.execute('SELECT * FROM ProductMovement').fetchall()
    return render_template("movement/list.html", movements=movements)

@bp.route('/new', methods=("GET",))
def create():
    # Get data from database
    products = get_all_products()
    locations = get_all_locations()

    # render movement form
    return render_template(
        'movement/make_movement.html', 
        products=products, 
        locations=locations
    )

@bp.route('/move', methods=("GET",))
def move():
    # Process the request data and 
    # save movement to database
    process_and_save_movement(request.args, "INSERT")

    # Notify the user
    flash("Product movement successfull!")

    # Redirect to all movements list
    return redirect(url_for('movement.index'))

@bp.route('/view/<movement_id>')
def view(movement_id: str):
    movement = get_movement(movement_id)
    return render_template('movement/details.html', movement=movement)

@bp.route('/edit/<movement_id>', methods=("GET", "POST"))
def edit(movement_id: str):
    if request.method == "GET":
        # Get data from database
        products = get_all_products()
        locations = get_all_locations()
        movement = get_movement(movement_id)

        # Get date and time string
        current_time = movement['timestamp'].strftime("%H:%M")
        current_date = movement['timestamp'].strftime("%Y-%m-%d")

        return render_template(
            'movement/edit.html', 
            movement=movement,
            products=products,
            locations=locations,
            current_date=current_date,
            current_time=current_time
        )
    else:
        # Process form data and 
        # update record in database
        process_and_save_movement(request.form, "UPDATE", movement_id=movement_id)
        # Notify user
        flash("Movement update successful!")
        # Redirect to movement list page
        return redirect(url_for('movement.index'))