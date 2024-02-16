import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError

scope = ['https://www.googleapis.com/auth/drive']

service_account_json_key = 'service_account_json_key.json'

credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key, 
                              scopes=scope)
service = build('drive', 'v3', credentials=credentials)

# results = service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)", q='name contains "de"').execute()

results = (service
            .files()
            .list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)")
            .execute())

items = results.get('files', [])

data = []
for row in items:
    if row["mimeType"] != "application/vnd.google-apps.folder":
        row_data = []
        try:
            row_data.append(round(int(row["size"])/1000000, 2))
        except KeyError:
            row_data.append(0.00)
        row_data.append(row["id"])
        row_data.append(row["name"])
        row_data.append(row["modifiedTime"])
        row_data.append(row["mimeType"])
        data.append(row_data)
cleared_df = pd.DataFrame(data, columns = ['size_in_MB', 'id', 'name', 'last_modification', 'type_of_file'])

print(cleared_df)
