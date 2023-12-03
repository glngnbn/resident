# app.py

from flask import Flask, render_template, redirect, url_for, session, request
from connection import DatabaseConnector
from login import Login
from dashboard import Dashboard
from appointment import Appointment
from update import Update
from medical import Medical

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret'

# Instantiate the DatabaseConnector class
db_connector = DatabaseConnector()

# Instantiate the Login, Dashboard, Appointment, Update, and Medical classes
dashboard_instance = Dashboard()
appointment_instance = Appointment(db_connector)
update_instance = Update()
medical_instance = Medical()

# Resident Page
@app.route('/', methods=['GET', 'POST'])
def login_route():
    return Login()

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_route():
    return dashboard_instance.dashboard()

@app.route('/dashboard/appointment', methods=['GET', 'POST'])
def appointment_route():
    return appointment_instance.process_appointment()

@app.route('/dashboard/update', methods=['GET', 'POST'])
def update_route():
    if request.method == 'POST':
        form_data = request.form  # Adjust this line based on your form data
        return update_instance.process_update(form_data)
    else:
        # Handle the GET request (if needed)
        return render_template("Residents/Update/update.html")

@app.route('/dashboard/medical', methods=['GET', 'POST'])
def medical_route():
    return medical_instance.process_medical()

# Log out
@app.route('/logout', methods=['POST'])
def logout():
    print("Before Logout:", session)
    session.pop('barangayid', None)
    print("After Logout:", session)
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    app.run(debug=True)
