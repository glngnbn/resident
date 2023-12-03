from flask import render_template, redirect, url_for, session, current_app
from connection import DatabaseConnector

class Dashboard:
    def __init__(self):
        self.db_connector = DatabaseConnector()

    def dashboard(self):
        # Check if 'barangayid' is in the session
        if 'barangayid' not in session:
            return redirect(url_for('login_route'))

        try:
            # Ensure 'barangayid' is a valid value (you may need additional validation)
            barangayid = session['barangayid']

            connection = self.db_connector.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT *
                FROM residentinfo
                JOIN addressinfo ON residentinfo.barangayid = addressinfo.barangayid
                JOIN appointment ON residentinfo.barangayid = appointment.barangayid
                WHERE residentinfo.barangayid = %s;
            """

            cursor.execute(query, (barangayid,))
            user_info = cursor.fetchone()

            if user_info:
                current_app.logger.info(f"User info: {user_info}")

                lastname = user_info['LastName']
                firstname = user_info['FirstName']
                middlename = user_info['MiddleName']

                category = user_info['Category']
                sex = user_info['Sex']
                contactno = user_info['ContactNo']

                voterprecinctno = user_info['VoterPrecinctNo']

                address = f"Purok {user_info['Zone']}, 0{user_info['HouseholdNo']} {user_info['StreetName']}, {user_info['City']} City"

                apstatus = user_info['status']

                # Assuming user_info[12] contains the relative file path
                relative_file_path = user_info['profile_picture']

                relative_file_path = user_info['profile_picture'].replace('\\', '/')

                if category == "student":
                    category = "Student"
                elif category == "adult":
                    category = "Adult"
                else:
                    category = "N/A"

                if sex == "male":
                    sex = "Male"
                elif sex == "Female":
                    sex = "Female"

                if voterprecinctno is None:
                    voterprecinctno = "None"
                else:
                    voterprecinctno = str(voterprecinctno)

                return render_template("Residents/Dashboard/dashboard.html", lastname=lastname, firstname=firstname,
                                       middlename=middlename, category=category, sex=sex, contactno=contactno,
                                       address=address, voterprecinctno=voterprecinctno, apstatus=apstatus,
                                       profile_picture=relative_file_path)
            else:
                return redirect(url_for('login_route'))
        except Exception as e:
            current_app.logger.error(f"An error occurred: {str(e)}")
            return render_template("error.html", message="An error occurred. Please try again later.")
