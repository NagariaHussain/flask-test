from flask import Blueprint, request, render_template, flash, redirect, abort
from flask.helpers import url_for
from inventory_manager.db import get_db

# Blueprint for '/location' endpoint
bp = Blueprint('location', __name__, url_prefix='/location')

def get_all_locations():
    '''return a list of all available locations in database'''
    db = get_db()
    sql_query = 'SELECT * FROM Location'
    locations = db.execute(sql_query).fetchall()

    return locations

def get_location(location_id: str):
    '''return a single location record with the given `location_id`,
       abort with 404, if not found'''
    # Get database connection instance
    db = get_db()
    select_sql_query = 'SELECT * FROM Location WHERE location_id = ?'
    location = db.execute(select_sql_query, (location_id,)).fetchone()

    # If location is not found
    if location is None:
        abort(404, f"Location: {location_id} Not Found!")

    return location


@bp.route('/', methods=('GET',))
def list_locations():
    locations = get_all_locations()
    # Render a page containing all locations
    return render_template('location/list.html', locations=locations)


@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == "POST":
        error_message = None
        # Add the location to database
        location_id = request.form['location_id']

        if not location_id:
            error_message = 'location_id is required!'
        
        if error_message is not None:
            flash(error_message)
        else:
            db = get_db()
            insert_sql_query = 'INSERT INTO location VALUES(?)'
            db.execute(insert_sql_query, (location_id,))
            db.commit()
            return redirect(url_for('location.list_locations'))
        
    # Render location addition form
    return render_template('location/add.html')
        
 
@bp.route('/view/<location_id>', methods=("GET",))
def view(location_id: str):
    location = get_location(location_id)

    # Render the details of the location
    return render_template('location/details.html', location=location)

@bp.route('/edit/<location_id>', methods=("GET", "POST"))
def edit(location_id: str):
    location = get_location(location_id)
    
    if request.method == "POST":
        new_location_id = request.form['location_id']

        if not new_location_id:
            flash('Please provide a location id!')

        update_sql_query = "UPDATE location SET location_id = ? WHERE location_id = ?"
        db = get_db()
        db.execute(update_sql_query, (new_location_id, location_id))
        db.commit()

        return redirect(url_for('location.list_locations'))

    # Render a pre populated form 
    # with location data
    return render_template('location/edit.html', location=location)
