# Flask imports
from flask import Blueprint, request, render_template, flash, redirect, abort
from flask.helpers import url_for

# Internal module imports
from inventory_manager.db import get_db

# Blueprint for '/location' endpoint
bp = Blueprint('location', __name__, url_prefix='/location')

# ------------------
# HELPER FUNCTIONS
# ------------------
def get_all_locations():
    '''return a list of all available locations in database'''
    # Get database connection instance
    db = get_db()
    # Fetch all locations 
    # sorted by location_id
    sql_query = 'SELECT * FROM Location ORDER BY location_id'
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

# ----------
# ROUTES
# ----------

# renders a list of all locations
@bp.route('/', methods=('GET',))
def list_locations():
    locations = get_all_locations()
    # Render a page containing all locations
    return render_template('location/list.html', locations=locations)

# GET: render create location form
# POST: save new location data
@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == "POST":
        error_message = None
        # Add the location to database
        location_id = request.form['location_id']

        # If location id is not provided 
        if not location_id:
            error_message = 'location_id is required!'
        
        # If there is a error message to show
        if error_message is not None:
            # show it to the user
            flash(error_message)
        # No error
        else:
            # Get db connection instance
            db = get_db()
            
            # Insert new record in location table
            insert_sql_query = 'INSERT INTO location VALUES(?)'
            db.execute(insert_sql_query, (location_id,))
            db.commit()

            # redirect to list locations page
            return redirect(url_for('location.list_locations'))
        
    # Render location addition form
    return render_template('location/add.html')
        
 
# View a particular location's details
@bp.route('/view/<location_id>', methods=("GET",))
def view(location_id: str):
    # Get particular location
    location = get_location(location_id)

    # Render the details of the location
    return render_template('location/details.html', location=location)

# GET: render edit location form
# POST: update given location with given data
@bp.route('/edit/<location_id>', methods=("GET", "POST"))
def edit(location_id: str):
    # Get data for a particular location
    location = get_location(location_id)
    
    if request.method == "POST":
        # Extract location_if from form data
        new_location_id = request.form['location_id']

        if not new_location_id:
            # Show flash message to user
            flash('Please provide a location id!')

        # Get db connection instance
        db = get_db()

        # Update db record
        update_sql_query = "UPDATE location SET location_id = ? WHERE location_id = ?"
        db.execute(update_sql_query, (new_location_id, location_id))
        db.commit()

        # redirect to list of locations page
        return redirect(url_for('location.list_locations'))

    # Render a pre populated form 
    # with location data
    return render_template('location/edit.html', location=location)
