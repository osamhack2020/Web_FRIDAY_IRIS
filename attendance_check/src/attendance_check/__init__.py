from flask import Flask
from attendance_check.models import get_db

app = Flask(__name__)
db = get_db(app)