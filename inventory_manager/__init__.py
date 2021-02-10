import os
from flask import Flask

def create_app():
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

    # Add blueprints
    from . import product, location, report
    app.register_blueprint(product.bp)
    app.register_blueprint(location.bp)
    app.register_blueprint(report.bp)
    app.add_url_rule('/', endpoint='index')
    
    # return this app instance
    return app
