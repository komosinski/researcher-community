from flask import Blueprint

bp = Blueprint('tag', __name__, template_folder='../../templates/tag')

from open_science.blueprints.tag import routes