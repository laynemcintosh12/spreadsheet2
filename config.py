import os

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'

# User credentials from environment variable
USER_CREDENTIALS = os.environ.get('USER_CREDENTIALS', '')

# Parse user credentials
def parse_user_credentials(credentials_str):
    users = {}
    for user_entry in credentials_str.split(';'):
        if ':' in user_entry:
            username, password = user_entry.split(':', 1)
            users[username] = password
    return users

USERS = parse_user_credentials(USER_CREDENTIALS)

# Google Sheets configuration
SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Sheets and their ranges
SHEETS = {
    'Projects': os.environ.get('PROJECTS_SHEET_RANGE', 'Projects!A2:P100'),
    'Balance Sheet': os.environ.get('BALANCE_SHEET_SHEET_RANGE', "'Balance Sheet'!A2:D50"),
    'YTD Tracker': os.environ.get('YTD_TRACKER_SHEET_RANGE', "Salesman!A2:F27")
}