from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
#Add BP routes here
from .blueprints.produce.routes import produce_bp
from .blueprints.contract.routes import contracts_bp
from .blueprints.shippinglabel.routes import shippinglabel_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.yaml'

swaggerui_blueprint= get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Produce & Shipping Management API"
    }
)


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    # add extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)



    #registering Blueprints
    app.register_blueprint(produce_bp, url_prefix='/produce')
    app.register_blueprint(contracts_bp, url_prefix='/contracts')# Fix this
    app.register_blueprint(shippinglabel_bp, url_prefix='/shippinglabel')
    #app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


    return app