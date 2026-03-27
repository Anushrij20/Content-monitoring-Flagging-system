# Content Monitoring & Flagging System

## Overview

This project is a backend system that ingests content, matches it against user-defined keywords, and generates flags for review.

It also supports reviewer decisions and ensures that previously marked irrelevant flags do not reappear unless the content has been updated.

---

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite (default database)

---

## Features

- Add keywords
- Scan content against keywords
- Generate flags with scores
- Reviewer can mark flags as:
  - pending
  - relevant
  - irrelevant
- Suppression logic:
  - Irrelevant flags are hidden
  - They reappear only if content is updated

---

## Project Structure

content_monitoring/
│
├── config/ # Django project settings
├── monitoring/ # Main app
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── services/
│ │ ├── ingest.py
│ │ ├── matching.py
│ │ └── scan.py
│
├── mock_data/
│ └── content.json # Sample content dataset
│
├── db.sqlite3
├── manage.py
└── requirements.txt


---

## Matching Logic

Scoring rules:

- Exact keyword match in title → 100
- Partial keyword match in title → 70
- Keyword found only in body → 40

---

## Suppression Logic

- When a flag is marked as `irrelevant`, it is suppressed.
- It will not appear in future scans.
- It will only reappear if:
  - the content item's `last_updated` is newer than when it was reviewed.

---

## Setup Instructions

### 1. Clone repository

git clone <your-repo-link>
cd <project-folder>


### 2. Create virtual environment


python -m venv venv
venv\Scripts\activate


### 3. Install dependencies


pip install -r requirements.txt


### 4. Apply migrations


python manage.py migrate


### 5. Run server


python manage.py runserver

Open:

http://127.0.0.1:8000/


---

## API Endpoints

### 1. Create Keyword


POST /api/keywords/

Example:

{"name": "python"}


---

### 2. Trigger Scan


POST /api/scan/

---

### 3. Get Flags


GET /api/flags/

---

### 4. Update Flag Status


PATCH /api/flags/{id}/


Example:


{"status": "irrelevant"}


---

## Sample Commands (PowerShell)

Create keyword:


Invoke-WebRequest -Method POST -Uri http://127.0.0.1:8000/api/keywords/
 -ContentType "application/json" -Body '{"name":"python"}' -UseBasicParsing


Run scan:


Invoke-WebRequest -Method POST -Uri http://127.0.0.1:8000/api/scan/
 -UseBasicParsing


Update flag:


Invoke-WebRequest -Method PATCH -Uri http://127.0.0.1:8000/api/flags/1/
 -ContentType "application/json" -Body '{"status":"irrelevant"}' -UseBasicParsing


---

## Data Source

- A mock JSON dataset is used (`mock_data/content.json`)
- This ensures reproducibility and simplicity

---

## Assumptions

- Each keyword-content pair creates only one flag
- Content is uniquely identified using `external_id`
- Suppression is based only on `last_updated`
- Resurfaced flags return to `pending` status

---

## Notes

- No frontend is included
- Focus is on backend correctness and clean architecture
- Logic is separated into services for clarity

---
