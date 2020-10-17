from attendance_check.views.groups import groups
from attendance_check.views.members import members
def register_db_api(app):
    app.register_blueprint(groups)
    app.register_blueprint(members)