from flask import Blueprint

shippinglabel_bp = Blueprint('shippinglabel_bp', __name__)

from . import routes