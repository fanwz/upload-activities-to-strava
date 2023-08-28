import requests
from stravalib.client import Client
import json
import os
import time
from flask import Flask, request
import sys
import webbrowser

CLIENT_ID = 'replace your client id here'
CLIENT_SECRET = 'replace your client secret here'


class TokenManager:
    def __init__(self, client_id, client_secret, filename="token_data.json"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.filename = filename
        self.client = Client()
        self.access_token = None
        self.refresh_token = None
        self.expires_at = 0  # Set it to 0 means it's expired by default.

        # Attempting to load token data from a file.
        self.load_from_file()

        # If the token has expired, attempt to refresh it.
        if self.is_token_expired():
            self.refresh_access_token()

    def is_token_expired(self):
        return time.time() > self.expires_at

    def refresh_access_token(self):
        response = self.client.refresh_access_token(client_id=self.client_id,
                                                    client_secret=self.client_secret,
                                                    refresh_token=self.refresh_token)
        self.access_token = response['access_token']
        self.refresh_token = response['refresh_token']
        self.expires_at = response['expires_at']
        self.client.access_token = self.access_token  # Update the client's access_token.
        self.save_to_file()

    def save_to_file(self, filename="token_data.json"):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'expires_human': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.expires_at)),
            'refreshed_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.access_token = data['access_token']
                self.refresh_token = data['refresh_token']
                self.expires_at = data['expires_at']
                self.client.access_token = self.access_token  # Update the client's access_token.
        else:
            self.get_token(self.client_id, self.client_secret)

    def get_token(self, client_id, client_secret, local_port: int = 8000):
        app = Flask(__name__)
        strava_client = Client()

        @app.route("/auth")
        def auth_callback():
            code = request.args.get('code')
            access_token = strava_client.exchange_code_for_token(
                client_id=client_id,
                client_secret=client_secret,
                code=code
            )

            self.access_token = access_token['access_token']
            self.refresh_token = access_token['refresh_token']
            self.expires_at = access_token['expires_at']
            self.save_to_file()

            print(access_token)
            ret_msg = "Access token: {token}<br>Refresh token: {refresh}<br>Expires at: {expires_at}<br>Expires human: {expires_human}<br>Refreshed at: {refreshed_at}".format(
                token=access_token['access_token'],
                refresh=access_token['refresh_token'],
                expires_at=access_token['expires_at'],
                expires_human=time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(access_token['expires_at'])),
                refreshed_at=time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            )
            ret_msg += "<br><br>Token data saved to token_data.json"
            ret_msg += "<br><br>Now you can close this window and go back to the CLI to close the local server(use ctrl+c)."
            ret_msg += "<br><br>Then the token data will be loaded from token_data.json and the token will automatically refresh the access token."
            ret_msg += "<br><br>After that, you can use the access token to upload activities to Strava."

            return ret_msg

        auth_url = strava_client.authorization_url(
            client_id=client_id,
            redirect_uri='http://127.0.0.1:{port}/auth'.format(
                port=local_port),
            scope=['activity:write', 'activity:read_all',
                   'profile:read_all', 'profile:write', 'read_all'],
            state='from_cli'
        )

        if sys.platform == 'darwin':
            print(
                'On OS X - launching {0} at default browser'.format(auth_url))
            subprocess.call(['open', auth_url])
        else:
            print('Go to {0} to authorize access: '.format(auth_url))
            webbrowser.open(auth_url)
        app.run(port=local_port)


class ActivityUploader:
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = Client(access_token=access_token)

    def upload_activity(self, file_path, data_type, activity_type, name, description):
        file = open(file_path, 'rb')
        ret = self.client.upload_activity(
            activity_file=file,
            data_type=data_type,
            activity_type=activity_type,
            name=name,
            description=description
        )

        # check the response of the upload request to see if it was successful
        if ret.response["error"] is None:
            print("Upload success!")
        else:
            print("Upload failed!")


if __name__ == "__main__":
    token = TokenManager(CLIENT_ID, CLIENT_SECRET)

    # upload activity
    uploader = ActivityUploader(token.access_token)
    uploader.upload_activity('your-activity-file.fit',
                             data_type='fit', activity_type='run', name='My Run', description='This is a test run')