from flask_babel import Babel
from flask_mail import Mail
from playhouse.flask_utils import FlaskDB

db = FlaskDB()
mail = Mail()

babel = Babel()
