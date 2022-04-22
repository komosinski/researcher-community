from flask import Blueprint

bp = Blueprint('action', __name__, template_folder='../../templates')

from open_science.blueprints.action import routes