from flask import Blueprint

bp = Blueprint('paper', __name__, template_folder='../../templates/article')

from open_science.blueprints.paper import routes