from attendance_check import app, db
from attendance_check.views import register_db_api

register_db_api(app)
app.run(host='0.0.0.0', debug=True)