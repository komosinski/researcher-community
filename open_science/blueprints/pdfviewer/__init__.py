from flask import Blueprint

bp = Blueprint('pdfviewer', __name__, template_folder='../../templates/pdfviewer')

from open_science.blueprints.pdfviewer import routes