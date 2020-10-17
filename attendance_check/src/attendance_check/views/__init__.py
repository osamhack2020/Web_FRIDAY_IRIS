from attendance_check.views.plznaming import plznaming

def register_db_api(app):
    app.register_blueprint(plznaming)