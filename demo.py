import datetime
from google_settings import create_service
from loader import CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES


service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
# print('Getting the upcoming 10 events')
# events_result = service.events().list(calendarId='pro100moneyfarmer@gmail.com', timeMin=now,
#                                     maxResults=10, singleEvents=True,
#                                     orderBy='startTime').execute()
# events = events_result.get('items', [])

# if not events:
#     print('No upcoming events found.')
# for event in events:
#     start = event['start'].get('dateTime', event['start'].get('date'))
#     print(start, event['summary'])