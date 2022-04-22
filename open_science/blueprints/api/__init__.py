from flask import Blueprint

bp = Blueprint('api', __name__)

from open_science.blueprints.api import routes