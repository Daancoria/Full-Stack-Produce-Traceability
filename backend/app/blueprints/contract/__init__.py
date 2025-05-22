from flask import Blueprint

contracts_bp = Blueprint('contracts_bp', __name__)

from . import routes