from flask import render_template

from open_science.blueprints.pdfviewer import bp



@bp.route('/pdfviewer')
def get_pdf_viewer():
    return render_template("pdfviewer/viewer.html")