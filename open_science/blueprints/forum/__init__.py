from flask import Blueprint

bp = Blueprint('forum', __name__, template_folder='../../templates')

from open_science.blueprints.forum import routes