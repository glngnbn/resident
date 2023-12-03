from flask import request, render_template, redirect, url_for, session
from connection import DatabaseConnector
db_pool = DatabaseConnector()
def Login():
    if request.method == 'POST':
        # Use a context manager to get a connection from the pool
        connection = db_pool.get_connection()
        cursor = connection.cursor()

        barangayid = request.form.get('barangayid')  # Use get to avoid KeyError
        session['barangayid'] = barangayid
        password = request.form.get('password')

        # Check credentials against the database
        query = "SELECT * FROM logininfo WHERE barangayid = %s AND password = %s"
        cursor.execute(query, (barangayid, password))
        user = cursor.fetchone()

        if user:
            # If user exists, render a success message
            return redirect(url_for('dashboard_route'))
        else:
            # If credentials are incorrect, render an error message
            return render_template('Residents/index.html', error="Incorrect password.")

    # If the request method is GET, render the login page
    return render_template('Residents/index.html')