from flask import Flask
from open_science.admin import MyAdminIndexView
from open_science.extensions import db, login_manager, \
    bcrypt, mail, limiter, admin, migrate, scheduler
import atexit
from config.config import Config


def register_extensions(app):
    db.init_app(app)
    db.app = app
    login_manager.init_app(app)
    login_manager.login_view = "login_page"
    login_manager.login_message_category = "info"
    bcrypt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    admin.init_app(app)
    admin.name = 'Admin Panel'
    admin.index_view = MyAdminIndexView()
    admin.template_mode = 'bootstrap4'
    migrate.init_app(app, db)
    scheduler.init_app(app)
    # #Two schedulers will be launched when Flask is in debug mode
    atexit.register(lambda: scheduler.shutdown())
    scheduler.start()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)

    return app


app = create_app()

# routes.pt is needed in this file but
# routes.py depends on __init__.py so to avoid circular imports
# we need to import routes at the bottom of the file.
# (we can also refactor the code to use blueprints to get rid of this import)
from open_science import routes, models
from open_science.schedule.schedule import daily_jobs, monthly_jobs

scheduler.add_job(
    id='Monthly jobs',
    func=monthly_jobs,
    start_date='2022-1-1 03:00:00',
    trigger='interval',
    days=31)

scheduler.add_job(
    id='Daily jobs',
    func=daily_jobs,
    start_date='2022-1-1 03:30:00',
    trigger='interval',
    days=1)
