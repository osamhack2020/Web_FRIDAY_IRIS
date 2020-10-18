from attendance_check.views.groups import groups
from attendance_check.views.members import members
from attendance_check.views.eatlogs import eatlogs
from attendance_check.views.date import date
def register_db_api(app):
    app.register_blueprint(groups)
    app.register_blueprint(members)
    app.register_blueprint(eatlogs)
    app.register_blueprint(date)