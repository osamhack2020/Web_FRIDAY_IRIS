from attendance_check.views.groups import groups
from attendance_check.views.members import members
from attendance_check.views.eatlogger import eatlogger
from attendance_check.views.date import date
from attendance_check.views.qr import qr
def register_api(app):
    app.register_blueprint(qr)
    app.register_blueprint(groups)
    app.register_blueprint(members)
    app.register_blueprint(eatlogger)
    app.register_blueprint(date)