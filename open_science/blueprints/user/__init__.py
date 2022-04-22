from flask import Blueprint

bp = Blueprint('user', __name__, template_folder='../../templates/user')

from open_science.blueprints.user import routes