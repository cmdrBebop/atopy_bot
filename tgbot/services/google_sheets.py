import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    def __init__(self, credentials_file: str, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        http_auth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    def add_customer(self, full_name: str, email: str, phone_number=''):
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='atopia!A1:C1',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={
                'values': [[full_name, email, phone_number]]
            }
        ).execute()
