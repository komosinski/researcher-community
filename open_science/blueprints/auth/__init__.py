from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='../../templates/user')

from open_science.blueprints.auth import routes