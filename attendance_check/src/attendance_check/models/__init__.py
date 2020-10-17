from attendance_check.models.models import *
from attendance_check.config import get_alchemy_uri

def get_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_alchemy_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db = SQLAlchemy(app)
    db.create_all()
    return db