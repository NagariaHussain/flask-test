from flask import Blueprint
from inventory_manager.db import get_db

bp = Blueprint('report', __name__)

# Home page with a report
@bp.route('/')
def index():
    return 'Home Page'