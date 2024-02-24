import warnings
warnings.simplefilter('ignore')

from gpiozero import LED
import time
import datetime
import os.path
import config

from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def authenticate():
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
        open_browser=config.openBrowserOnAuthentication,
        success_message='Success! You may now close the browser!'
      )
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds

def fetchEvents(service):
  now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
  nowPlus12 = (datetime.datetime.utcnow() + datetime.timedelta(hours=config.numberOfHoursAhead)).isoformat() + "Z" # 12 hours after the minimum time

  print("Getting the upcoming events for the next 12 hours")
  events_result = (
    service.events()
      .list(
         calendarId=config.calendarId,
         timeMin=now,
         timeMax=nowPlus12,
         singleEvents=True,
         orderBy="startTime",
      )
    .execute()
  )
  return events_result.get("items", [])

def main():
  if (config.testLEDOnStartup):
    sign = LED(config.LEDPin)
    sign.on()
    time.sleep(2)
    sign.off()
  
  creds = authenticate()

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    events = fetchEvents(service)

    # Prints the start and name of the next 10 events
    for event in events:
      # start = event["start"].get("dateTime", event["start"].get("time"))
      print(event["start"].get("dateTime"))

    count = 0
    while True:
      inMeeting = False

      for event in events:
        if (datetime.datetime.fromisoformat(event["start"].get("dateTime")) < datetime.datetime.now(datetime.timezone.utc) and
        datetime.datetime.fromisoformat(event["end"].get("dateTime")) > datetime.datetime.now(datetime.timezone.utc)):
          inMeeting = True

      if (inMeeting): sign.on()
      else: sign.off()

      count += 1
      if(count == config.fetchingFrequencyHours * 36):
        events = fetchEvents(service)
        count = 0

      time.sleep(10)
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()
