from flask import Blueprint

produce_bp = Blueprint('produce_bp', __name__)

from . import routes 