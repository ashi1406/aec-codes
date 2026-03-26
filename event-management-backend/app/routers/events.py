# backend/app/routers/events.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app import models, schemas
from app.services import email_service

router = APIRouter()

@router.get("/", response_model=dict)
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all events with pagination and filters"""
    query = db.query(models.Event)
    
    if search:
        query = query.filter(models.Event.name.ilike(f"%{search}%"))
    if type:
        query = query.filter(models.Event.type == type)
    if status:
        query = query.filter(models.Event.status == status)
    
    total = query.count()
    events = query.offset(skip).limit(limit).all()
    
    return {
        "data": events,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{event_id}", response_model=schemas.Event)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event by ID"""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/", response_model=schemas.Event, status_code=201)
async def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create new event"""
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/{event_id}", response_model=schemas.Event)
async def update_event(
    event_id: int,
    event: schemas.EventUpdate,
    db: Session = Depends(get_db)
):
    """Update event"""
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete event"""
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}

@router.post("/{event_id}/register/{participant_id}")
async def register_participant(
    event_id: int,
    participant_id: int,
    db: Session = Depends(get_db)
):
    """Register participant for event"""
    # Check if event exists
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if participant exists
    participant = db.query(models.Participant).filter(
        models.Participant.id == participant_id
    ).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    # Check if already registered
    existing = db.query(models.EventParticipant).filter(
        models.EventParticipant.event_id == event_id,
        models.EventParticipant.participant_id == participant_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already registered")
    
    # Check capacity
    current_count = db.query(models.EventParticipant).filter(
        models.EventParticipant.event_id == event_id
    ).count()
    
    if current_count >= event.max_participants:
        raise HTTPException(status_code=400, detail="Event is full")
    
    # Register
    registration = models.EventParticipant(
        event_id=event_id,
        participant_id=participant_id
    )
    db.add(registration)
    
    # Update current participants count
    event.current_participants = current_count + 1
    
    db.commit()
    
    # Send confirmation email (async)
    email_service.send_registration_confirmation(participant, event)
    
    return {"message": "Registration successful"}

@router.put("/{event_id}/score/{participant_id}")
async def update_score(
    event_id: int,
    participant_id: int,
    score: float,
    db: Session = Depends(get_db)
):
    """Update participant score for event"""
    registration = db.query(models.EventParticipant).filter(
        models.EventParticipant.event_id == event_id,
        models.EventParticipant.participant_id == participant_id
    ).first()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    registration.score = score
    db.commit()
    
    return {"message": "Score updated successfully"}