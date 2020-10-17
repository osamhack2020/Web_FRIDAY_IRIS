from attendance_check.views.groups import groups

def register_db_api(app):
    app.register_blueprint(groups)