# backend/scripts/seed_all.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Venue, Event, Participant, EventParticipant, User
from datetime import datetime, timedelta
import random
import bcrypt

def seed_database():
    db = SessionLocal()
    
    print("🌱 Seeding database...")
    
    # Clear existing data
    print("Clearing existing data...")
    db.query(EventParticipant).delete()
    db.query(Participant).delete()
    db.query(Event).delete()
    db.query(Venue).delete()
    db.query(User).delete()
    
    # Create venues
    print("Creating venues...")
    venues = [
        Venue(
            name="Main Auditorium",
            capacity=500,
            location="Ground Floor, Main Building",
            building="Main Building",
            floor=0,
            has_projector=True,
            has_sound_system=True,
            has_ac=True,
            has_wifi=True,
            contact_person="John Smith",
            contact_phone="1234567890"
        ),
        Venue(
            name="Seminar Hall A",
            capacity=200,
            location="First Floor, Academic Block",
            building="Academic Block",
            floor=1,
            has_projector=True,
            has_sound_system=True,
            has_ac=True,
            has_wifi=True,
            contact_person="Jane Doe",
            contact_phone="1234567891"
        ),
        Venue(
            name="Conference Room",
            capacity=50,
            location="Second Floor, Admin Block",
            building="Admin Block",
            floor=2,
            has_projector=True,
            has_sound_system=False,
            has_ac=True,
            has_wifi=True,
            contact_person="Bob Wilson",
            contact_phone="1234567892"
        ),
        Venue(
            name="Open Air Theatre",
            capacity=1000,
            location="Campus Grounds",
            building="Grounds",
            floor=0,
            has_projector=False,
            has_sound_system=True,
            has_ac=False,
            has_wifi=False,
            contact_person="Alice Brown",
            contact_phone="1234567893"
        ),
        Venue(
            name="Lab 101",
            capacity=30,
            location="First Floor, Lab Complex",
            building="Lab Complex",
            floor=1,
            has_projector=True,
            has_sound_system=False,
            has_ac=True,
            has_wifi=True,
            contact_person="Charlie Davis",
            contact_phone="1234567894"
        ),
    ]
    
    for venue in venues:
        db.add(venue)
    db.commit()
    
    # Create events
    print("Creating events...")
    now = datetime.now()
    events = [
        Event(
            name="Tech Symposium 2024",
            description="Annual technical symposium with coding competitions, workshops, and talks",
            type="technical",
            status="planned",
            start_date=now + timedelta(days=10),
            end_date=now + timedelta(days=12),
            registration_deadline=now + timedelta(days=8),
            venue_id=1,
            coordinator="Dr. Sarah Johnson",
            coordinator_email="sarah.j@college.edu",
            coordinator_phone="9876543210",
            max_participants=200,
            budget=50000.0,
            requirements=["projector", "sound_system", "wifi"],
            banner_image="/images/tech-symposium.jpg"
        ),
        Event(
            name="Cultural Night 2024",
            description="Annual cultural event featuring music, dance, and drama performances",
            type="cultural",
            status="planned",
            start_date=now + timedelta(days=15),
            end_date=now + timedelta(days=15, hours=6),
            registration_deadline=now + timedelta(days=12),
            venue_id=4,
            coordinator="Prof. Michael Chen",
            coordinator_email="michael.c@college.edu",
            coordinator_phone="9876543211",
            max_participants=300,
            budget=30000.0,
            requirements=["sound_system", "stage"],
            banner_image="/images/cultural-night.jpg"
        ),
        Event(
            name="Sports Meet 2024",
            description="Inter-department sports competition",
            type="sports",
            status="planned",
            start_date=now + timedelta(days=20),
            end_date=now + timedelta(days=22),
            registration_deadline=now + timedelta(days=15),
            venue_id=4,
            coordinator="Mr. David Wilson",
            coordinator_email="david.w@college.edu",
            coordinator_phone="9876543212",
            max_participants=150,
            budget=25000.0,
            requirements=["sound_system"],
            banner_image="/images/sports-meet.jpg"
        ),
        Event(
            name="AI/ML Workshop",
            description="Hands-on workshop on Artificial Intelligence and Machine Learning",
            type="workshop",
            status="planned",
            start_date=now + timedelta(days=5),
            end_date=now + timedelta(days=7),
            registration_deadline=now + timedelta(days=3),
            venue_id=5,
            coordinator="Dr. Emily Brown",
            coordinator_email="emily.b@college.edu",
            coordinator_phone="9876543213",
            max_participants=30,
            budget=15000.0,
            requirements=["projector", "wifi", "computers"],
            banner_image="/images/ai-workshop.jpg"
        ),
        Event(
            name="Research Symposium",
            description="Research paper presentations by students and faculty",
            type="seminar",
            status="completed",
            start_date=now - timedelta(days=5),
            end_date=now - timedelta(days=5, hours=8),
            registration_deadline=now - timedelta(days=10),
            venue_id=2,
            coordinator="Dr. Robert Lee",
            coordinator_email="robert.l@college.edu",
            coordinator_phone="9876543214",
            max_participants=100,
            budget=10000.0,
            requirements=["projector", "sound_system"],
            banner_image="/images/research-symposium.jpg"
        ),
    ]
    
    for event in events:
        db.add(event)
    db.commit()
    
    # Create participants
    print("Creating participants...")
    departments = ['CSE', 'ECE', 'MECH', 'CIVIL', 'EEE', 'IT', 'CHEM']
    first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Chris', 'Lisa', 'Tom', 'Amy']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    participants = []
    for i in range(1, 101):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"student{i}@college.edu"
        dept = random.choice(departments)
        year = random.randint(1, 4)
        roll = f"{dept}{2024000+i}"
        
        participant = Participant(
            name=name,
            email=email,
            phone=f"98765{random.randint(10000, 99999)}",
            department=dept,
            year=year,
            roll_number=roll,
            address=f"Hostel Block {random.choice(['A','B','C','D'])}, Room {random.randint(101, 500)}",
            city="Tech City",
            emergency_contact_name=f"Parent of {name}",
            emergency_contact_phone=f"98765{random.randint(10000, 99999)}"
        )
        participants.append(participant)
        db.add(participant)
    
    db.commit()
    
    # Register participants for events
    print("Registering participants...")
    for event in events:
        num_participants = random.randint(20, min(50, event.max_participants))
        selected = random.sample(participants, num_participants)
        
        for participant in selected:
            ep = EventParticipant(
                event_id=event.id,
                participant_id=participant.id,
                score=random.uniform(60, 100) if event.status == "completed" else 0
            )
            db.add(ep)
        
        event.current_participants = num_participants
    
    db.commit()
    
    # Create admin user
    print("Creating admin user...")
    hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    admin = User(
        username="admin",
        email="admin@college.edu",
        hashed_password=hashed,
        full_name="System Administrator",
        role="admin",
        is_active=True
    )
    db.add(admin)
    
    # Create coordinator users
    coordinators = [
        ("coordinator1", "coord1@college.edu", "Sarah Johnson"),
        ("coordinator2", "coord2@college.edu", "Michael Chen"),
        ("coordinator3", "coord3@college.edu", "David Wilson"),
    ]
    
    for username, email, name in coordinators:
        hashed = bcrypt.hashpw("coord123".encode(), bcrypt.gensalt()).decode()
        coordinator = User(
            username=username,
            email=email,
            hashed_password=hashed,
            full_name=name,
            role="coordinator",
            is_active=True
        )
        db.add(coordinator)
    
    db.commit()
    
    print("✅ Database seeded successfully!")
    print(f"📊 Created: {len(venues)} venues")
    print(f"📊 Created: {len(events)} events")
    print(f"📊 Created: {len(participants)} participants")
    print(f"📊 Created: {db.query(EventParticipant).count()} registrations")
    print(f"👤 Created: admin user (username: admin, password: admin123)")
    print(f"👤 Created: coordinator users (password: coord123)")

if __name__ == "__main__":
    seed_database()