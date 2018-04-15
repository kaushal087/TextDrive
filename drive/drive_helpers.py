from __future__ import print_function
import  json
import uuid
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
from av.models import Folder
from django.conf import settings

class DriveHelper(object):

    def __init__(self, request=None):
        self.request = request
        self.user = request.user
        self.folder = Folder.objects.filter(user_id=self.user.id).first()

        credentials_dict = settings.CREDENTIALS_DICT
        if(self.user):
            social_data = self.user.social_auth.first().extra_data
            credentials_dict['refresh_token'] = social_data.get('refresh_token')
            credentials_dict['access_token'] = social_data.get('access_token')

        store = file.Storage(data=json.dumps(credentials_dict))
        creds = store.get()
        if not creds or creds.invalid:
            raise Exception

        self.service = build('drive', 'v3', http=creds.authorize(Http()))


    def _create_folder(self):
        file_metadata = {
            'name': 'av_notes',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()

        file_id = file.get('id')
        user_id = self.request.user.id

        Folder.objects.create(folder_id=file_id, user_id=user_id)


    def get_list(self):
        files = []
        data = {}

        # if folder is not created: create folder and return empty list
        if self.folder is None:
            self._create_folder()
            data['files'] = files
            return data

        data['folder_id'] = self.folder.folder_id

        page_token = None

        while True:
            q = "'" + data['folder_id'] + "' in parents"
            response = self.service.files().list(q=q,
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute()
            for file in response.get('files', []):
                files.append({'file_id':file.get('id'), 'name':file.get('name')})
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        data['files'] = files
        return data


    def get_file_content(self, file_id):
        try:
            file_data = self.service.files().get(fileId=file_id).execute()
            content = self.service.files().get_media(fileId=file_id).execute()
            file_data['content'] = content.decode("utf-8")
            return file_data
        except Exception:
            print("error occured in fetching content")

    def _get_random_string(self):
        return "temp/" + str(uuid.uuid4().hex) + ".txt"

    def _create_temp_file(self, data):
        content = data.get('content')
        temp_file_name = self._get_random_string()
        base_dir = os.path.dirname(__file__)
        temp_file_fullpath = os.path.join(base_dir, temp_file_name)
        f = open(temp_file_fullpath, "w+")
        f.write(content)
        f.close()
        return temp_file_fullpath

    def _delete_temp_file(self, file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass


    def update_file(self, file_id, data):
        file_name = data.get('file_name', 'Untitled.txt')

        file_path = self._create_temp_file(data)

        file_metadata = {
            'name': file_name
        }

        media = MediaFileUpload(filename=file_path,
                                mimetype='text/plain',
                                resumable=True)
        file = self.service.files().update(fileId=file_id, body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()

        self._delete_temp_file(file_path)
        return file


    def create_file(self, data):
        file_name = data.get('file_name', 'Untitled.txt')
        file_path = self._create_temp_file(data)
        folder_id = self.folder.folder_id
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(filename=file_path,
                                mimetype='text/plain',
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        self._delete_temp_file(file_path)
        return file


    def update_or_create_file(self, file_id=None, data=None):
        if(file_id):
            self.update_file(file_id=file_id, data=data)
        else:
            self.create_file(data=data)
