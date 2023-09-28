from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread


class GoogleApi():

    def __init__(self) -> None:

        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'] # Can be modified
        self.SPREADSHEET_ID = "<your_spreadsheet_id>"  # Can be find in sheet url

    def authentication_authorization(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)  # Obtained from GCP
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def update_spreadsheet(self, range_name, value_input_option, _values):
        """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
            """
        creds = self.authentication_authorization()

        try:

            service = build('sheets', 'v4', credentials=creds)
            values = _values
            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID, range=range_name,
                valueInputOption=value_input_option, body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")

            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def clear_and_insert(self, dataframe):

        creds = self.authentication_authorization()

        gc = gspread.authorize(credentials=creds)
        worksheet = gc.open_by_key(self.SPREADSHEET_ID).sheet1
        worksheet.clear()
        worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
