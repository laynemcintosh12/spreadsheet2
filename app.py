import os
import base64
import json
from flask import Flask, render_template, request, redirect, url_for, session
from google.oauth2 import service_account
from googleapiclient.discovery import build
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Google Sheets setup
# Decode the Base64 encoded JSON string from environment variable
service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
if service_account_json:
    service_account_json = base64.b64decode(service_account_json).decode('utf-8')
    credentials_info = json.loads(service_account_json)
else:
    raise ValueError("Service account JSON is not set in environment variables.")

creds = service_account.Credentials.from_service_account_info(credentials_info)
service = build('sheets', 'v4', credentials=creds)

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('data', sheet='Projects'))  # Redirect to the updated sheet name
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in config.USERS and config.USERS[username] == password:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('data', sheet='Projects'))  # Redirect to the updated sheet name
    return redirect(url_for('home'))

@app.route('/data/<sheet>')
def data(sheet):
    if 'logged_in' not in session:
        return redirect(url_for('home'))

    if sheet not in config.SHEETS:
        return redirect(url_for('data', sheet='Projects'))

    # Get the sheet range for the selected sheet
    range_name = config.SHEETS[sheet]

    # Access the Google Sheets API and get the data
    sheet_service = service.spreadsheets()
    result = sheet_service.values().get(spreadsheetId=config.SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])

    # Assuming the first row contains headers
    if values:
        headers = values[0]
        data_rows = values[1:]

        # Filter out rows where all cells are empty, '0', or '$0.00'
        def is_relevant(row):
            return any(cell and cell not in {'0', '$0.00', ''} for cell in row)

        filtered_data_rows = [row for row in data_rows if is_relevant(row)]
    else:
        headers = []
        filtered_data_rows = []

    return render_template('data.html', headers=headers, values=filtered_data_rows, sheet=sheet)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.context_processor
def inject_navbar():
    return dict(sheets=config.SHEETS)

if __name__ == '__main__':
    app.run(debug=True)