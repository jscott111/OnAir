from gpiozero import LED
import time
import datetime
import os.path

from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  sign = LED(26)
  sign.on()
  time.sleep(2)
  sign.off()
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(
	host='localhost',
	port=8080,
	open_browser=False,
	success_message='Success! You may now close the browser!'
)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 5 events")
    events_result = (
        service.events()
        .list(
            calendarId="js@heyorca.com",
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      # start = event["start"].get("dateTime", event["start"].get("time"))
      print(event["start"].get("dateTime"))

    while True:
      print("Checking")
      inMeeting = False

      for event in events:
        if (datetime.datetime.fromisoformat(event["start"].get("dateTime")) < datetime.datetime.now(datetime.timezone.utc) and
        datetime.datetime.fromisoformat(event["end"].get("dateTime")) > datetime.datetime.now(datetime.timezone.utc)):
          inMeeting = True

      if (inMeeting): sign.on()
      else: sign.off()
      time.sleep(10)
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()