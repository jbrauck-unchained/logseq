from datetime import datetime
import dateutil.parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    """Authenticate and return the Google Calendar service."""
    creds = None
    # If token.json exists, load the credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

def fetch_meetings(service, day):
    """Fetch meetings for a given day."""
    start_time = datetime.combine(day, datetime.min.time()).isoformat() + 'Z'
    end_time = datetime.combine(day, datetime.max.time()).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=start_time, timeMax=end_time,
        singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])
    return events

def generate_template(event):
    """Generate Logseq meeting template for a Google Calendar event."""
    title = event.get('summary', 'Untitled Meeting')
    date = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date'))).strftime('%H:%M')
    
    blocks = [
        (f"## Meeting: {title} #meeting", 0),
        (f"**Time:** {date}", 1),
        ("**Topics Discussed**", 1),
        ("**Action Items**", 1),
        ("[ ] Task 1", 1),
        ("[ ] Task 2", 1),
        ("**Notes**", 1),
    ]
    return blocks


def save_to_logseq(blocks, date, journal_dir="/Users/joe-unchained/Documents/journals"):
    """Save generated templates to a Logseq markdown file."""
    # Format the date for the filename: YYYY_MM_DD.md
    filename = date.strftime('%Y_%m_%d.md')
    filepath = os.path.join(journal_dir, filename)
    
    # Create directory if it doesn't exist
    os.makedirs(journal_dir, exist_ok=True)
    
    # Convert blocks into properly formatted markdown with correct indentation
    markdown_lines = []
    for content, level in blocks:
        indentation = "  " * level
        markdown_lines.append(f"{indentation}- {content}\n")
    
    # Append to the file (create if doesn't exist)
    with open(filepath, 'a') as f:
        f.write("\n")
        f.writelines(markdown_lines)
        f.write("\n")

def main():
    # Authenticate Google Calendar API
    service = authenticate_google_calendar()

    # Get today's date
    today = datetime.utcnow().date()

    # Fetch meetings for today
    events = fetch_meetings(service, today)

    # Generate and add blocks for each meeting
    for event in events:
        if event['summary'] != 'Home' and event['summary'] != 'Concierge Blockout':
            blocks = generate_template(event)
            save_to_logseq(blocks, today)

if __name__ == '__main__':
    main()
