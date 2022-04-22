from flask import Blueprint

bp = Blueprint('search', __name__, template_folder='../../templates/search')

from open_science.blueprints.search import routes