from flask import Blueprint, render_template

page_routes = Blueprint('page_routes', __name__)

@page_routes.route('/')
def index():
    return render_template('Modules/Main/Start/login.html')

@page_routes.route('/send_items')
def send_items():
    return render_template('Modules/Main/Handover/handover.html')

@page_routes.route('/welcome')
def welcome():
    return render_template('Modules/Main/Start/welcome.html')

@page_routes.route('/return_to_login')
def return_to_login():
    return render_template('Modules/Main/Start/login.html')

@page_routes.route('/transactionhistory')
def transactionhistory():
    return render_template('Modules/Main/Transaction History/transactionHistory.html')

@page_routes.route('/transferprogresstable')
def transferprogresstable():
    return render_template('Modules/Main/Transaction Progress/transferprogresstable.html')

@page_routes.route('/approvetable')
def approvetable():
    return render_template('Modules/Main/Approval/approvalTable.html')

@page_routes.route('/approve_table')
def approve_table():
    return render_template('approvalTable.html')

@page_routes.route('/invent')
def invent():
    return render_template('Modules/Main/Dashboard/invent.html')

@page_routes.route('/project_invent')
def project_invent():
    return render_template('Modules/Main/Dashboard/project_invent.html')

@page_routes.route('/my_invent')
def my_invent():
    return render_template('Modules/Main/Dashboard/my_invent.html')

@page_routes.route('/receive_form_data')
def receive_form_data():
    return render_template('Modules/Main/Receiver/form_data.html')

@page_routes.route('/receive_table')
def receive_table():
    return render_template('Modules/Main/Receiver/recieveTable.html')

@page_routes.route('/transaction_history_form_data')
def transaction_history_form_data():
    return render_template('Modules/Main/Transaction History/transaction_history_form_data.html')

@page_routes.route('/display_send_approval')
def display_send_approval():
    return render_template('Modules/Main/Approval/approve_send_form_data.html')

@page_routes.route('/display_receive_approval')
def display_receive_approval():
    return render_template('Modules/Main/Approval/approve_receive_form_data.html')

@page_routes.route('/display_transaction_progess_table')
def display_transaction_progess_table():
    return render_template('Modules/Main/Transaction Progress/transactionprogressform.html')
