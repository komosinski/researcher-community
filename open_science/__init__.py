#from flask_migrate import migrate
from flask import Flask
from open_science.admin import MyAdminIndexView
from open_science.extensions import db, login_manager,bcrypt, mail, limiter, scheduler, admin, migrate
import atexit
from config import Config


def register_extensions(app):
    db.init_app(app)
    #TODO: check if it doesn't break anything
    db.app = app 
    #
    login_manager.init_app(app)
    login_manager.login_view = "login_page"
    login_manager.login_message_category = "info"
    bcrypt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    admin.init_app(app)
    admin.name = 'Admin Panel'
    admin.index_view = MyAdminIndexView()
    admin.template_mode='bootstrap4'
    migrate.init_app(app,db)
    scheduler.init_app(app)
    # #Two schedulers will be launched when Flask is in debug mode
    atexit.register(lambda: scheduler.shutdown())
    
  
def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    register_extensions(app)

    return app

app = create_app()
from open_science import routes, models

from open_science.schedule.schedule import daily_jobs, monthly_jobs
scheduler.add_job(id ='Monthly jobs', func = monthly_jobs, start_date='2022-1-1 03:00:00', trigger = 'interval', days = 31)
scheduler.add_job(id ='Daily jobs', func = daily_jobs, start_date='2022-1-1 03:30:00', trigger = 'interval', days = 1)
scheduler.start()