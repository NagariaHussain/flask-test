from flask import Blueprint, request, render_template, flash, redirect, abort
from flask.helpers import url_for
from inventory_manager.db import get_db

# Blueprint for '/movement' endpoint
bp = Blueprint('movement', __name__, url_prefix='/movement')

@bp.route('/', methods=("GET",))
def create():
    return render_template('make_movement.html')