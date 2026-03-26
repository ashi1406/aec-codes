# backend/tests/test_events.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.main import app
from app.database import Base, get_db
from app.models import Event, Venue, Participant

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestEvents:
    @classmethod
    def setup_class(cls):
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create test data
        db = TestingSessionLocal()
        
        # Create venue
        venue = Venue(
            name="Test Venue",
            capacity=100,
            location="Test Location",
            has_projector=True,
            has_sound_system=True
        )
        db.add(venue)
        db.commit()
        
        cls.venue_id = venue.id
        
        # Create event
        event = Event(
            name="Test Event",
            description="Test Description",
            type="technical",
            start_date=datetime.now() + timedelta(days=10),
            end_date=datetime.now() + timedelta(days=10, hours=5),
            coordinator="Test Coordinator",
            max_participants=50,
            venue_id=venue.id
        )
        db.add(event)
        db.commit()
        
        cls.event_id = event.id
        
        # Create participant
        participant = Participant(
            name="Test Participant",
            email="test@example.com",
            department="CSE",
            year=3,
            roll_number="TEST001"
        )
        db.add(participant)
        db.commit()
        
        cls.participant_id = participant.id
        
        db.close()
    
    @classmethod
    def teardown_class(cls):
        # Drop tables
        Base.metadata.drop_all(bind=engine)
    
    def test_get_events(self):
        response = client.get("/events/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
    
    def test_get_event_by_id(self):
        response = client.get(f"/events/{self.event_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Event"
    
    def test_create_event(self):
        new_event = {
            "name": "New Event",
            "description": "New Description",
            "type": "cultural",
            "start_date": (datetime.now() + timedelta(days=20)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=20, hours=4)).isoformat(),
            "coordinator": "New Coordinator",
            "max_participants": 100,
            "venue_id": self.venue_id
        }
        
        response = client.post("/events/", json=new_event)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Event"
    
    def test_update_event(self):
        update_data = {
            "name": "Updated Event",
            "max_participants": 75
        }
        
        response = client.put(f"/events/{self.event_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Event"
        assert data["max_participants"] == 75
    
    def test_register_participant(self):
        response = client.post(
            f"/events/{self.event_id}/register/{self.participant_id}"
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Registration successful"
    
    def test_update_score(self):
        response = client.put(
            f"/events/{self.event_id}/score/{self.participant_id}",
            params={"score": 85.5}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Score updated successfully"
    
    def test_delete_event(self):
        response = client.delete(f"/events/{self.event_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Event deleted successfully"

class TestVenues:
    def test_get_venues(self):
        response = client.get("/venues/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
    
    def test_check_availability(self):
        start = (datetime.now() + timedelta(days=5)).isoformat()
        end = (datetime.now() + timedelta(days=5, hours=3)).isoformat()
        
        response = client.get(
            f"/venues/{self.venue_id}/availability",
            params={"start": start, "end": end}
        )
        assert response.status_code == 200
        assert "available" in response.json()

class TestParticipants:
    def test_get_participants(self):
        response = client.get("/participants/")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
    
    def test_create_participant(self):
        new_participant = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "department": "ECE",
            "year": 2,
            "roll_number": "TEST002"
        }
        
        response = client.post("/participants/", json=new_participant)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Jane Doe"

class TestScores:
    def test_get_leaderboard(self):
        response = client.get("/scores/leaderboard")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_event_scores(self):
        response = client.get(f"/scores/event/{self.event_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_department_stats(self):
        response = client.get("/scores/department-stats")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)