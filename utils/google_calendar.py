import datetime
import json
import os.path
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from starlette.responses import JSONResponse

from config.config import GOOGLE_API_KEY

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.events"]


async def get_events(google_token):
    creds = google_token

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", 'w') as token_file:
            token_file.write(creds.to_json())

        try:
            service = build("calendar", "v3", credentials=creds)
            now = datetime.datetime.now().isoformat() + "Z"
            event_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True,
                                                 orderBy="startTime").execute()
            events = event_result.get("items", [])

            if not events:
                return

            for event in events:
                start = event["start"].get("datetime", event["start"].get("date"))

        except HttpError as error:
            pass


async def create_service():
    creds = None
    if os.path.exists("utils/token.json"):
        creds = Credentials.from_authorized_user_file("utils/token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("utils/credentials.json", SCOPES)
            # creds = flow.run_local_server(port=0)
            # creds = flow.run_local_server(host="10.0.2.59", port=8000)
            creds = flow.run_local_server(port=8080)

        with open("utils/token.json", 'w') as token_file:
            token_file.write(creds.to_json())

    return creds


async def create_event(google_token, id, organizer, room, description, start_time, end_time, guests):
    start_time = str(start_time)
    end_time = str(end_time)
    api_key = GOOGLE_API_KEY
    try:
        event_body = {
            "id": id,
            "summary": description,
            "location": room,
            "description": f"You were invited to meeting {description} organized by {organizer}.\n"
                           f"Meeting get place in {room} at {start_time} and continue until {end_time}",
            "colorId": 6,
            "status": "confirmed",
            "start": {
                "dateTime": f"{start_time.split(sep=' ')[0]}T{start_time.split(sep=' ')[1]}",
                "timeZone": "Asia/Tashkent"
            },
            "end": {
                "dateTime": f"{end_time.split(sep=' ')[0]}T{end_time.split(sep=' ')[1]}",
                "timeZone": "Asia/Tashkent"
            },
            "organizer": {
                "displayName ": organizer,
                "self": False
            },
            "attendees": guests
        }
        headers = {
            'Authorization': f'Bearer {google_token}',
            'Content-Type': 'application/json',
        }
        url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events?key={api_key}"
        event = requests.post(url=url, headers=headers, data=json.dumps(event_body))
    except HttpError as error:
        JSONResponse({"Message": "Error occured with Google calendar Api"})


async def delete_event(id, google_token):
    api_key = GOOGLE_API_KEY
    try:
        url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events/{id}?key={api_key}"
        headers = {
            'Authorization': f'Bearer {google_token}',
            'Content-Type': 'application/json',
        }
        deleted_event = requests.delete(url=url, headers=headers)
    except HttpError as error:
        JSONResponse({"Message": "Error occured with Google calendar Api"})
