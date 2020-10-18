from attendance_check import app, db
from attendance_check.views import register_db_api
from flask import render_template

register_db_api(app)
@app.route('/', methods=['GET'])
def read_qrcode():
    return render_template("index.html")
app.run(host='0.0.0.0', debug=True)