# Std lib imports
import os

# Flask imports
from flask import Flask

def create_app():
    '''creates, configures and returns a flask app instances'''
    # Create flask instance
    app = Flask(__name__, instance_relative_config=True)

    # Set secret and db config
    app.config.from_mapping(
        SECRET_KEY='cool-secret',
        DATABASE=os.path.join(app.instance_path, 'inventory.sqlite'),
    )

    # Create instance dirs and files
    # (if not already exists)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize database connection
    from . import db
    db.init_app(app)

    # Import blueprints libs
    from . import product, location, report, product_movement

    # Add blueprints
    app.register_blueprint(product.bp)
    app.register_blueprint(location.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(product_movement.bp)

    # To make '/' equivalent 
    # to 'index' (for url_for)
    app.add_url_rule('/', endpoint='index')
    
    # return this app instance
    return app
