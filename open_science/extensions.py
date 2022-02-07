from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apscheduler import APScheduler
from flask_admin import Admin
from flask_migrate import Migrate
from flask_moment import Moment

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
limiter = Limiter(key_func=get_remote_address,
                  default_limits=["100 per minute"])
scheduler = APScheduler()
admin = Admin()
migrate = Migrate()
# moment.js for showing dates
moment = Moment()

