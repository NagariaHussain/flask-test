from flask import Blueprint, request, render_template, flash, redirect
from flask.helpers import url_for
from inventory_manager.db import get_db

# Blueprint for '/location' endpoint
bp = Blueprint('location', __name__, url_prefix='/location')


@bp.route('/', methods=('GET',))
def list_locations():
    db = get_db()
    sql_query = 'SELECT * FROM Location'
    locations = db.execute(sql_query).fetchall()
    
    # For Debugging
    print(locations)

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
        
