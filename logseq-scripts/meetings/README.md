# Logseq Daily Meetings Notes Script

This script automatically generates Logseq meeting note templates from your Google Calendar events. It's designed to be run daily to create structured meeting notes for all your calendar events.

## Features

- Authenticates with Google Calendar API
- Fetches meetings for the current day
- Generates Logseq-formatted meeting templates with:
  - Meeting title and time
  - Topics discussed section
  - Action items section
  - Notes section
- Saves templates to your Logseq journals directory

## Getting Started

### Prerequisites

- Python 3.6 or higher
- A Google Cloud project with Calendar API enabled
- Logseq installed with a journals directory set up

### Installation

1. Clone this repository
2. Install required packages:
