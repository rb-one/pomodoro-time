from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
