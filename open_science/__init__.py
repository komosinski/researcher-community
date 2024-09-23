from re import L
from flask import Flask, request, flash, abort
from open_science.admin import MyAdminIndexView
from open_science.extensions import db, login_manager, \
    bcrypt, mail, limiter, admin, migrate, scheduler, moment
from config.config import Config
import atexit
from open_science.admin import MyModelView, UserView, MessageToStaffView


def register_extensions(app):
    db.init_app(app)
    db.app = app
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"
    login_manager.refresh_view = "auth.login_page"
    login_manager.login_message_category = "info"
    login_manager.needs_refresh_message_category = "info"
    bcrypt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    admin.init_app(app)
    admin.name = 'Admin Panel'
    admin.index_view = MyAdminIndexView()
    admin.template_mode = 'bootstrap4'
    migrate.init_app(app, db)
    scheduler.init_app(app)
    moment.init_app(app)

    from open_science.models import MessageToStaff, User, PaperRevision, Tag, Review, ReviewRequest, Comment, ForumTopic
    admin.add_view(MessageToStaffView(MessageToStaff, db.session))  # custom endpoints can be defined by an argument, e.g., endpoint='messagetostaff_'. Otherwise, by default, endpoints will be named in lowercase after the table names.
    admin.add_view(UserView(User, db.session))
    admin.add_view(MyModelView(PaperRevision, db.session))
    admin.add_view(MyModelView(Tag, db.session))
    admin.add_view(MyModelView(Review, db.session))
    admin.add_view(MyModelView(ReviewRequest, db.session))
    admin.add_view(MyModelView(Comment, db.session))
    admin.add_view(MyModelView(ForumTopic, db.session))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)

    # BLUEPRINTS
    from open_science.blueprints.tag import bp as tag_bp
    app.register_blueprint(tag_bp, url_prefix='/tag')

    from open_science.blueprints.database import bp as db_bp
    app.register_blueprint(db_bp)

    from open_science.blueprints.notification import bp as notif_bp
    app.register_blueprint(notif_bp)

    from open_science.blueprints.review import bp as rev_bp
    app.register_blueprint(rev_bp)

    from open_science.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from open_science.blueprints.search import bp as search_bp
    app.register_blueprint(search_bp)

    from open_science.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from open_science.blueprints.user import bp as user_bp
    app.register_blueprint(user_bp)

    from open_science.blueprints.action import bp as action_bp
    app.register_blueprint(action_bp)

    from open_science.blueprints.paper import bp as paper_bp
    app.register_blueprint(paper_bp)

    from open_science.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    from open_science.blueprints.pdfviewer import bp as pdfviewer_bp
    app.register_blueprint(pdfviewer_bp)

    from open_science.blueprints.forum import bp as forum_bp
    app.register_blueprint(forum_bp)

    return app


app = create_app()
app.app_context().push()


@app.before_request
def check_read_only():
    excluded_routes = ['/login']
    if request.path in excluded_routes:
        return None
    if app.config['READONLY_MODE'] and request.method in ['POST', 'PUT', 'DELETE']:
        flash('The application is in read-only mode. Editing is disabled.')
        abort(403, description="The application is in read-only mode. Editing is disabled.")



# importing add_scheduler_jobs earlier causes circular imports
from open_science.schedule.schedule import add_scheduler_jobs

if app.config['START_SCHEDULER'] is True and scheduler.running is False:
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    add_scheduler_jobs()
    print("Scheduler is running")

from open_science import models
