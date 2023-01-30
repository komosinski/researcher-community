import time

from flask import render_template, redirect, url_for, flash, abort, request
from open_science.blueprints.search import bp
from open_science.blueprints.search.forms import AdvancedSearchPaperForm, \
    AdvancedSearchUserForm, AdvancedSearchTagForm
from open_science.blueprints.search import helpers as search_helper
from open_science.utils import check_numeric_args
import ast
from open_science.models import Review
from open_science.blueprints.database.db_helper import get_hidden_filter


@bp.route('/search/results')
def search_papers_page():
    search_text = request.args.get('search_text')
    search_like = "%{}%".format(search_text)
    search_option = request.args.get('search_option', 'title')
    rows_per_page = request.args.get('rows_per_page', 5, type=int)
    page_num = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by')

    order = search_helper.get_paper_order(order_by)
    paper_revisions = search_helper.get_papers_basic_search(
        search_like, search_option, order, page_num, rows_per_page)

    if not paper_revisions:
        flash('No results found!', category='warning')
        return redirect(url_for('main.home_page'))

    return render_template("search/search_paper_result_list.html", papers=paper_revisions)


@bp.route('/search/advanced')
def advanced_search_page():
    paper_form = AdvancedSearchPaperForm(request.args)
    user_form = AdvancedSearchUserForm(request.args)
    tag_form = AdvancedSearchTagForm(request.args)

    # TODO Add error validation messages
    if paper_form.submit_paper.data and paper_form.validate():
        search_data = paper_form.data
        return redirect(url_for('search.advanced_search_papers_page', page=1, search_data=search_data, order_by='newest'))
    elif user_form.submit_user.data and user_form.validate():
        search_data = user_form.data
        return redirect(url_for('search.advanced_search_users_page', page=1, search_data=search_data, order_by='score'))
    elif tag_form.submit_tag.data and tag_form.validate():
        search_data = tag_form.data
        return redirect(url_for('search.advanced_search_tags_page', page=1, search_data=search_data, order_by='newest'))

    return render_template('/search/advanced_search.html', paper_form=paper_form, user_form=user_form,
                           tag_form=tag_form)


@bp.route('/search/advanced/papers/<page>/<search_data>/<order_by>')
def advanced_search_papers_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if not check_numeric_args(page):
        abort(404)

    if isinstance(page, str):
        page = int(page)

    papers = []
    order = search_helper.get_paper_order(order_by)
    papers = search_helper.get_papers_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_paper.html', page=page, papers=papers, search_data=search_data,
                           order_by=order_by)


@bp.route('/search/advanced/users/<page>/<search_data>/<order_by>')
def advanced_search_users_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if not check_numeric_args(page):
        abort(404)

    page = int(page)

    users = []
    start = time.time()
    order = search_helper.get_user_order(order_by)
    users = search_helper.get_users_advanced_search(page, search_data, order)
    end = time.time()
    print(f"time: {end - start}")

    return render_template('search/advanced_search_user.html', page=page, users=users, search_data=search_data,
                           order_by=order_by)


@bp.route('/search/advanced/tags/<page>/<search_data>/<order_by>')
def advanced_search_tags_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if not check_numeric_args(page):
        abort(404)

    page = int(page)

    tags = []
    order = search_helper.get_tag_order(order_by)
    tags = search_helper.get_tags_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_tag.html', page=page, tags=tags, search_data=search_data,
                           order_by=order_by)


@bp.route('/search/reviews/<page>/<search_data>/<order_by>')
def reviews_list_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if not check_numeric_args(page):
        abort(404)

    page = int(page)
    user_id = int(search_data['user_id'])
    reviews = []
    order = Review.publication_datetime.desc()
    reviews = Review.query.filter(Review.creator == user_id,
                                  get_hidden_filter(Review),
                                  Review.is_anonymous == False,
                                  Review.publication_datetime != None).order_by(order).paginate(page=page, per_page=30)

    if reviews.pages == 0:
        return redirect(url_for('user.profile_page', user_id=user_id))

    return render_template('search/review_result_list.html', page=page, reviews=reviews, search_data=search_data,
                           order_by=order_by)
