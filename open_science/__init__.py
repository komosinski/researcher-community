from re import L
from flask import Flask
from open_science.admin import MyAdminIndexView
from open_science.extensions import db, login_manager, \
    bcrypt, mail, limiter, admin, migrate, scheduler
from config.config import Config
import atexit


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

# also importing add_scheduler_jobs earlier causes circular imports
from open_science.schedule.schedule import add_scheduler_jobs
if app.config['START_SCHEDULER'] is True and scheduler.running is False:
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    add_scheduler_jobs()
    print("Scheduler is running")
