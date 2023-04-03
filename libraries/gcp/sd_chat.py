from googleapiclient.discovery import build

import google.auth

CREDENTIALS, PROJECT_ID = google.auth.default()

class ChatClient:

    def __init__(self):
        self.credentials = CREDENTIALS.with_scopes(
            ['https://www.googleapis.com/auth/chat.bot'])
        self.chat = build('chat', 'v1', credentials=self.credentials)

    def send_message_to_user(self, space_name, text):

        try:
            self.chat.spaces().messages().create(
                parent=space_name,
                body={"text": text}).execute()
        except:
            pass

        return
