"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Drive v3 API
#SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive.appfolder'

credentials_dict = {
    "access_token": "ya29.GlucBUPBrS1slQ4BguPyjujBY47YRoxhYPQZcZd_35hvW_89SWTuIEzPyoSsLQOvgGZ6PTom2JWowNc86__5I2mcUJmj7YMJIi_syF8CqLv5xvuTuKiW6h7g-YZ0",
    "client_id": "841703207471-hc7p5vt5fe2g7ulq0073lgp7c54qmvbq.apps.googleusercontent.com",
    "client_secret": "sIQ1-e_itDEtAKVLv0IXCWna",
    "refresh_token": "1/ZQ6HRl8xL3DYhJGh0gL4-pAof3APnAihFV69s9JDNbwc9k7wthFL3W91fAyL-rsU",
    "token_expiry": "2018-04-13T22:12:16Z",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "user_agent": None,
    "revoke_uri": "https://accounts.google.com/o/oauth2/revoke",
    "id_token": {
        "azp": "841703207471-hc7p5vt5fe2g7ulq0073lgp7c54qmvbq.apps.googleusercontent.com",
        "aud": "841703207471-hc7p5vt5fe2g7ulq0073lgp7c54qmvbq.apps.googleusercontent.com",
        "sub": "101790226644244358304",
        "email": "kaushal499@gmail.com",
        "email_verified": True,
        "at_hash": "jJ48RahQxGssMIXvJUDLUw",
        "exp": 1523657536,
        "iss": "accounts.google.com",
        "iat": 1523653936
    },
    "id_token_jwt": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNiNTQ3ODg2ZmY4NWEzNDI4ZGY0ZjYxZGI3M2MxYzIzOTgyYTkyOGUifQ.eyJhenAiOiI4NDE3MDMyMDc0NzEtaGM3cDV2dDVmZTJnN3VscTAwNzNsZ3A3YzU0cW12YnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4NDE3MDMyMDc0NzEtaGM3cDV2dDVmZTJnN3VscTAwNzNsZ3A3YzU0cW12YnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDE3OTAyMjY2NDQyNDQzNTgzMDQiLCJlbWFpbCI6ImthdXNoYWw0OTlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJqSjQ4UmFoUXhHc3NNSVh2SlVETFV3IiwiZXhwIjoxNTIzNjU3NTM2LCJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNTIzNjUzOTM2fQ.LunplSlbOJjcoN3b0GB5Jn-WyMGt5LiHalpfWNSBnZYoknUUS01ZQwoixIEP55Z63LtXtzNsYOj-xjYjYulLswTcwfLz4skVZbwGE9X06jNai9pd-TyTo1ai4tAB_zdPmuTz3SsM201HNLYpFbY6sKla3RkZlM6CuMh5dE3_UPHBkv3vqPZcQVkCS3LedJL4uHs9nu7BQrBFmvV4xM7t2lxoUCNXvHJMOi0ZOHuq46O1rPiGiD1a7SImiEaeXdRs-ug9zgNDLjiIN2Cgeey-7EM4MI61XEVKUxVXJnVoU8EFuvnOcxKXRM5QWJnwumEbh5WuGYiaRBwGyydQ9PKWUA",
    "token_response": {
        "access_token": "ya29.GlucBUPBrS1slQ4BguPyjujBY47YRoxhYPQZcZd_35hvW_89SWTuIEzPyoSsLQOvgGZ6PTom2JWowNc86__5I2mcUJmj7YMJIi_syF8CqLv5xvuTuKiW6h7g-YZ0",
        "expires_in": 3600,
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNiNTQ3ODg2ZmY4NWEzNDI4ZGY0ZjYxZGI3M2MxYzIzOTgyYTkyOGUifQ.eyJhenAiOiI4NDE3MDMyMDc0NzEtaGM3cDV2dDVmZTJnN3VscTAwNzNsZ3A3YzU0cW12YnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4NDE3MDMyMDc0NzEtaGM3cDV2dDVmZTJnN3VscTAwNzNsZ3A3YzU0cW12YnEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDE3OTAyMjY2NDQyNDQzNTgzMDQiLCJlbWFpbCI6ImthdXNoYWw0OTlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJqSjQ4UmFoUXhHc3NNSVh2SlVETFV3IiwiZXhwIjoxNTIzNjU3NTM2LCJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNTIzNjUzOTM2fQ.LunplSlbOJjcoN3b0GB5Jn-WyMGt5LiHalpfWNSBnZYoknUUS01ZQwoixIEP55Z63LtXtzNsYOj-xjYjYulLswTcwfLz4skVZbwGE9X06jNai9pd-TyTo1ai4tAB_zdPmuTz3SsM201HNLYpFbY6sKla3RkZlM6CuMh5dE3_UPHBkv3vqPZcQVkCS3LedJL4uHs9nu7BQrBFmvV4xM7t2lxoUCNXvHJMOi0ZOHuq46O1rPiGiD1a7SImiEaeXdRs-ug9zgNDLjiIN2Cgeey-7EM4MI61XEVKUxVXJnVoU8EFuvnOcxKXRM5QWJnwumEbh5WuGYiaRBwGyydQ9PKWUA",
        "token_type": "Bearer"
    },
    "scopes": [
        "https://www.googleapis.com/auth/drive.appfolder"
    ],
    "token_info_uri": "https://www.googleapis.com/oauth2/v3/tokeninfo",
    "invalid": False,
    "_class": "OAuth2Credentials",
    "_module": "oauth2client.client"
}
import  json
store = file.Storage(data=json.dumps(credentials_dict))
print(store)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive v3 API
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
folder_created = False
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))
        if item['name'] == 'AV':
            folder_created = True


if not folder_created:
    file_metadata = {
        'name': 'AV',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % file.get('id'))

