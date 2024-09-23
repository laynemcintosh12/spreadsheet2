import os
import base64

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
SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON', '')
if SERVICE_ACCOUNT_JSON:
    # Ensure the length of the Base64 string is a multiple of 4 by adding necessary padding
    missing_padding = len(SERVICE_ACCOUNT_JSON) % 4
    if missing_padding:
        SERVICE_ACCOUNT_JSON += '=' * (4 - missing_padding)
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Sheets and their ranges
SHEETS = {
    'Projects': os.environ.get('PROJECTS_SHEET_RANGE', 'Projects!A2:W2000'),
    'Balance Sheet': os.environ.get('BALANCE_SHEET_SHEET_RANGE', "'Balance Sheet'!A2:E50"),
    'YTD Tracker': os.environ.get('YTD_TRACKER_SHEET_RANGE', "Salesman!A2:F27"),
    'Finalized': os.environ.get('FINALIZED_SHEET_RANGE', "Finalized!A2:W2000"),
    'Supplements': os.environ.get('SUPPLEMENTS_SHEET_RANGE', "'Supplement Dashboard'!A2:P2000"),
}
