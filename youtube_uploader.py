from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Function to authenticate and create a YouTube service
def get_authenticated_service():
    credentials = None
    # Token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print("Loading Credentials From File...")
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
            print("Crendentials loaded.")

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            print("Fetching New Tokens...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json',
                scopes=[
                    'https://www.googleapis.com/auth/youtube.upload'
                ]
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)

    return build('youtube', 'v3', credentials=credentials)

# Function to upload a video
def upload_video(file_path, title, description, category, tags):
    youtube = get_authenticated_service()

    request_body = {
        'snippet': {
            'categoryI': category,
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private'
        }
    }

    mediaFile = MediaFileUpload(file_path)

    print("Performing upload now ... please wait.")
    response_upload = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    return response_upload

# Example Usage:
# upload_video('path_to_video.mp4', 'My Video Title', 'This is a description', '22', ['tag1', 'tag2'])
