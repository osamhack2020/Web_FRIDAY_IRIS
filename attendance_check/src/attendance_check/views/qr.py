from flask import Blueprint, render_template
qr = Blueprint('qr', __name__, url_prefix='/qr')
@qr.route('/scan/', methods=['GET'])
def show_qr_reader():
    return render_template("qr_scan.html")