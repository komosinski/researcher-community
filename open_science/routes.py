from werkzeug.wrappers import request
from open_science import app
from open_science import routes_def as rd
from open_science.test_data import create_test_data
from open_science.user import routes_def as user_rd
from open_science.user import api as user_api
from open_science.tag import api as tag_api
from open_science.review import routes_def as review_rd
from open_science.tag import routes_def as tag_rd
from open_science.notification import routes_def as notif_rd
from flask_login import login_required
from open_science import limiter
from flask import render_template


# TODO: remove this temporary variable and read the state from another source
VAR = False

@app.before_request
def before_req():
    if VAR:
        return render_template("maintenance.html")

@app.route("/t")
def test():
    if create_test_data():
        return "test data has been created"
    return "test data already exists"


@app.route("/")
def home_page():
    return rd.home_page()


@limiter.limit("2 per second")
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return user_rd.register_page()


@limiter.limit("2 per second")
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return user_rd.login_page()


@app.route('/logout')
@login_required
def logout_page():
    return user_rd.logout_page()


@app.route('/confirm-email/<token>')
def confirm_email(token):
    return user_rd.confirm_email(token)


@app.route('/user/unconfirmed', methods=['GET', 'POST'])
def unconfirmed_email_page():
    return user_rd.unconfirmed_email_page()


@limiter.limit("2 per second")
@app.route('/user/account-recovery', methods=['GET', 'POST'])
def account_recovery_page():
    return user_rd.account_recovery_page()


@app.route('/user/set-password/<token>', methods=['GET', 'POST'])
def set_password_page(token):
    return user_rd.set_password_page(token)


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def profile_page(user_id):
    return user_rd.profile_page(user_id)


@app.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile_page():
    return user_rd.edit_profile_page()


@app.route('/user/change_password', methods=['GET', 'POST'])
@login_required
def change_password_page():
    return user_rd.change_password_page()


@app.route('/email_change_confirmation/<token>', methods=['GET', 'POST'])
def confirm_email_change(token):
    return user_rd.confirm_email_change(token)


@app.route('/article/<id>/', methods=['GET', 'POST'])
def article(id):
    return rd.view_article(id)


@app.route('/article/add', methods=['GET', 'POST'])
@login_required
@rd.researcher_user_required
def upload_file_page():
    return rd.file_upload_page()


@app.route('/action/like', methods=['POST'])
def addLike():
    return rd.like()
# # TODO: complete this endpoint
# @app.route('/article/add', methods=['POST'])
# def uploadArticle():
#     return rd.uploadArticle(request)


@app.route('/search/results')
def search_papers_page():
    return rd.search_papers_page()


@app.route('/search/advanced')
def advanced_search_page():
    return rd.advanced_search_page()


@app.route('/search/advanced/papers/<page>/<search_data>/<order_by>')
def advanced_search_papers_page(page, search_data, order_by):
    return rd.advanced_search_papers_page(page, search_data, order_by)


@app.route('/search/advanced/users/<page>/<search_data>/<order_by>')
def advanced_search_users_page(page, search_data, order_by):
    return rd.advanced_search_users_page(page, search_data, order_by)


@app.route('/search/advanced/tags/<page>/<search_data>/<order_by>')
def advanced_search_tags_page(page, search_data, order_by):
    return rd.advanced_search_tags_page(page, search_data, order_by)


@app.route('/search/reviews/<page>/<search_data>/<order_by>')
def reviews_list_page(page, search_data, order_by):
    return rd.reviews_list_page(page, search_data, order_by)


@app.route('/user/invite', methods=['GET', 'POST'])
@login_required
def invite_user_page():
    return user_rd.invite_user_page()


@app.route('/help/faq')
def faq_page():
    return rd.faq_page()


@app.route('/help')
def help_page():
    return rd.help_page()


@app.route('/help/contact', methods=['GET', 'POST'])
@login_required
def contact_staff_page():
    return rd.contact_staff_page()


@app.route('/api/user_papers')
@login_required
@rd.researcher_user_required
def user_papers_data():
    return user_api.user_papers_data()


@app.route('/review/request/<request_id>', methods=['GET', 'POST'])
@login_required
def review_request_page(request_id):
    return review_rd.review_request_page(request_id)


@app.route('/user/notifications/<page>/<unread>')
@login_required
def notifications_page(page, unread):
    return notif_rd.notifications_page(page, unread)


@app.route('/endorsement/request/<endorser_id>')
@login_required
def request_endorsement(endorser_id):
    return user_rd.request_endorsement(endorser_id)


@app.route('/endorsement/confirm/<notification_id>/<user_id>/<endorser_id>', methods=['GET', 'POST'])
@login_required
@rd.researcher_user_required
def confirm_endorsement_page(notification_id, user_id, endorser_id):
    return user_rd.confirm_endorsement_page(notification_id, user_id, endorser_id)


@app.route('/review/edit/<review_id>', methods=['GET', 'POST'])
@login_required
@rd.researcher_user_required
def review_edit_page(review_id):
    return review_rd.review_edit_page(review_id)


@app.route('/user/notifications/update')
@login_required
def update_notification_and_redirect():
    return notif_rd.update_notification_and_redirect()


@app.route('/api/user_reviews')
@login_required
@rd.researcher_user_required
def user_reviews_data():
    return user_api.user_reviews_data()


@app.route('/tag/create', methods=['GET', 'POST'])
@login_required
@rd.researcher_user_required
def create_tag_page():
    return tag_rd.create_tag_page()


@app.route('/tag/edit/<tag_id>', methods=['GET', 'POST'])
@login_required
@rd.researcher_user_required
def edit_tag_page(tag_id):
    return tag_rd.edit_tag_page(tag_id)


@app.route('/review/<review_id>',)
def review_page(review_id):
    return review_rd.review_page(review_id)


@app.route('/review/hide/<review_id>', methods=['GET', 'POST'])
@login_required
@rd.researcher_user_required
def hide_review(review_id):
    return review_rd.hide_review(review_id)


@app.route('/api/user_tags')
@login_required
@rd.researcher_user_required
def user_tags_data():
    return user_api.user_tags_data()


@app.route('/api/user_comments')
@login_required
def user_comments_data():
    return user_api.user_comments_data()


@app.route('/tag/<tag_name>')
def tag_page(tag_name):
    return tag_rd.tag_page(tag_name)


@app.route('/user/delete_profile', methods=['GET', 'POST'])
@login_required
def delete_profile_page():
    return user_rd.delete_profile_page()


@app.route('/user/delete_profile/confirm/<token>')
@login_required
def confirm_profile_delete(token):
    return user_rd.confirm_profile_delete(token)


@app.route('/api/tags')
def get_all_tags_data():
    return tag_api.get_all_tags_data()


@app.route('/test')
def test_text_preprocessing():
    return rd.test_text_preprocessing()

