from flask import Blueprint

bp = Blueprint('review', __name__, template_folder='../../templates/review')

from open_science.blueprints.review import routes