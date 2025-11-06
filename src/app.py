"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports activities
    "Soccer Team": {
        "description": "Competitive soccer team practicing drills and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["ryan@mergington.edu", "lia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team practices and inter-school competitions",
        "schedule": "Mondays, Wednesdays, 4:30 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["mason@mergington.edu", "ava@mergington.edu"]
    },
    # Artistic activities
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["zoe@mergington.edu", "liam@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, play production, and stagecraft",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["natalie@mergington.edu", "ethan@mergington.edu"]
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Practice public speaking, argumentation, and debate tournaments",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["chris@mergington.edu", "harper@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, science fairs, and STEM projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity (normalize email and prevent duplicates)"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Normalize the provided email (trim and lowercase) to avoid duplicates by case/whitespace
    normalized_email = email.strip().lower()

    # Get the specific activity
    activity = activities[activity_name]

    # Build a set of normalized existing participant emails
    existing = {p.strip().lower() for p in activity.get("participants", [])}

    # Validate student is not already signed up
    if normalized_email in existing:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Optionally check capacity
    if len(activity.get("participants", [])) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add normalized student email
    activity.setdefault("participants", []).append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
