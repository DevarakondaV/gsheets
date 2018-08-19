from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow,argparser
from oauth2client.file import Storage

class gsheets:

    def __init__(self,col_names,client_id,client_secret,sheet_id = None):
        if not isinstance(col_names,list):
            raise TypeError("Col_names parameter must be list")
        self.client_id = client_id
        self.client_secret = client_secret        
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        self.col_names = col_names
        self._authenticate_get_creds()
        if sheet_id is None:
            self._new_sheet_id()
        else:
            self.SPREADSHEET_ID = sheet_id
        print(self.SPREADSHEET_ID)
        self._add_titles()

    #Cloud API Functions
    def _authenticate_get_creds(self):
        """
        Creates flow, and gets credentials for API
        """
        flow = OAuth2WebServerFlow(client_id = self.client_id,
                                    client_secret = self.client_secret,
                                    scope=self.SCOPES,
                                    redirect_uri="http://example.com/auth_return")
        storage = Storage('creds.data')
        flags = argparser.parse_args(args=[])
        self.credentials = run_flow(flow,storage,flags=flags)
        self.service = build('sheets','v4',http=self.credentials.authorize(Http()))

    def __check_creds(self):
        if not self.credentials or self.credentials.invalid:
            self._authenticate_get_creds()
    
    def _new_sheet_id(self):
        """
            If user does not specify a new spread sheet, creates new sheet and saves the ID"
        """
        self.__check_creds()
        sheet_body = { 'properties':{
            'title': "ML_Project_Updates"}
        }
        response = self.service.spreadsheets().create(body=sheet_body).execute()
        self.SPREADSHEET_ID = response["spreadsheetId"]
        return
    
    def _add_titles(self):
        self.__check_creds()
        gsheets_titals = [self.col_names,]
        body = {
            'values': gsheets_titals
        }
        response = self.service.spreadsheets().values().append(spreadsheetId=self.SPREADSHEET_ID,range="A1",
                                                                valueInputOption='USER_ENTERED',body=body).execute()
        return


    #Functions for adding to google sheets
    def add_values(self,dict_values):
        self.__check_creds()        
        values = self._parse_new_values(dict_values)
        body = {
            'values': values
        }
        response = self.service.spreadsheets().values().append(spreadsheetId=self.SPREADSHEET_ID,range="A1",
                                                                valueInputOption='USER_ENTERED',body=body).execute()
        return


    def _parse_new_values(self,dict_values):
        """
        Arranges values in dict_values to the correct order to push to sheets.
        
        args:
            dict_values: Dictionary. Values to be adde to sheets
        
        Returns:
            return the values in dict_values in correct order for sheets
        """
        keys = list(dict_values.keys())
        if keys != self.col_names:
            raise ValueError("Dictionary Keys does not contain same names. Or is not the same size")
        
        new_vals = [dict_values[i] for i in self.col_names]
        gsheets_vals = [new_vals,]
        return gsheets_vals


    #Access/Modifier methods
    def get_sheet_id(self):
        return self.SPREADSHEET_ID

    def set_sheet_id(self,sheet_id):
        self.SPREADSHEET_ID = sheet_id
        return
