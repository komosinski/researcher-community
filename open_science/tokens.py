from itsdangerous import URLSafeTimedSerializer
from open_science import app

def generate_password_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

# throws exception if failed
def confirm_password_token(token, expiration=7200):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )

    return email

def generate_account_recovery_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_ACCOUNT_RECOVERY_SALT'])

# throws exception if failed
def confirm_account_recovery_token(token, expiration=7200):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
  
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_ACCOUNT_RECOVERY_SALT'],
        max_age=expiration
    )

    return email

def generate_email_change_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_CHANGE_EMAIL_SALT'])

# throws exception if failed
def confirm_email_change_token(token, expiration=7200):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
  
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_CHANGE_EMAIL_SALT'],
        max_age=expiration
    )
  
    return email