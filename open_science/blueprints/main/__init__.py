from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='../../templates')

from open_science.blueprints.main import routes