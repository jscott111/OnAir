# On Air

This is a personal project for a raspberry pi which will connect to and fetch from my Google calendar to be able to light up a sign when I am in a meeting.

For this project you will need:
- A Raspberry Pi
- IO cables
- LED or sign that you can wire up to the raspberry pi and turn it on or off with the GPIO.
- Make sure you have a [Google Cloud Project](https://developers.google.com/workspace/guides/create-project)

## Setup
First you will need to clone this repo into your Raspberry Pi

Once that is done, make sure you have Python > `3.10.7` installed

Ensure you also have `pip`

Once those have been confirmed, run this code:

    pip -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib, gpiozero

Enable the [Google Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)

Configure the [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
- Add your account as a test user

Create your [OAuth Credentials](https://console.cloud.google.com/apis/credentials)
- Create credentials for OAuth client ID
- Make sure the application type is `Desktop App`
- Save the credentials into a file called `credentials.json` and store it in the repo you cloned

## Running the Code

Run this code:

    cp config-template.py config.py

Open the new config.py file and add your Calendar's name to the `calendarId` field, you should be able to see this in the left panel when viewing you Google Cal on your desktop, or in general in your list of Calendars
- You can also change some of the values you see in the config file as well, specifically which pin you will have you LED connected to

Connect your light with the GPIO cables to the pin you have indicated in the config file
- If you left `testLEDOnStartup = True` then you should see the light turn on for 2 seconds when you first start the program

## IT'S TIIIIME

Do this next step while on the Raspberry Pi GUI, either through VNC or a connected monitor

Execute:

    python3 OnAir.py

This should open your browser if you left `openBrowserOnAuthentication = True`, if there is an issue, open your config file and change it to `False`. This will generate a URL which you can open and follow the steps there to login and authenticate the program to do what it needs to do

Once that completes and you see `Success! You may now close the browser!`, you can close the browser and should be able to see the start times of your meetings for the next 12 hours printed out to the console.

There you go, you did it!

If you have any questions or run into some trouble, please contact me and I will do my best to help you set it up!

