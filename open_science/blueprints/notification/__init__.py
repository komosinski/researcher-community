from flask import Blueprint

bp = Blueprint('notification', __name__, template_folder='../../templates/notification')

from open_science.blueprints.notification import routes