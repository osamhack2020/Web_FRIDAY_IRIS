from flask import Flask
from flask_migrate import Migrate
from attendance_check.models import get_db

app = Flask(__name__)
# Support UTF8
app.config['JSON_AS_ASCII'] = False
db = get_db(app)
migrate = Migrate(app, db)