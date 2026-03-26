# backend/app/services/score_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict
from app.models import EventParticipant, Participant, Event
from app.services.email_service import email_service

class ScoreService:
    def __init__(self, db: Session):
        self.db = db
    
    def update_score(self, event_id: int, participant_id: int, score: float):
        """Update participant score for event"""
        registration = self.db.query(EventParticipant).filter(
            EventParticipant.event_id == event_id,
            EventParticipant.participant_id == participant_id
        ).first()
        
        if registration:
            registration.score = score
            self.db.commit()
            
            # Send notification
            participant = self.db.query(Participant).get(participant_id)
            event = self.db.query(Event).get(event_id)
            email_service.send_score_notification(participant, event, score)
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get overall leaderboard"""
        results = self.db.query(
            Participant.id,
            Participant.name,
            Participant.department,
            func.count(EventParticipant.event_id).label('events_count'),
            func.sum(EventParticipant.score).label('total_score'),
            func.avg(EventParticipant.score).label('avg_score')
        ).join(
            EventParticipant
        ).group_by(
            Participant.id
        ).order_by(
            desc('total_score')
        ).limit(limit).all()
        
        leaderboard = []
        for i, r in enumerate(results, 1):
            leaderboard.append({
                'rank': i,
                'id': r.id,
                'name': r.name,
                'department': r.department,
                'events_count': r.events_count,
                'total_score': float(r.total_score or 0),
                'avg_score': float(r.avg_score or 0)
            })
        
        return leaderboard
    
    def get_event_scores(self, event_id: int) -> List[Dict]:
        """Get scores for specific event"""
        results = self.db.query(
            Participant.id,
            Participant.name,
            Participant.department,
            EventParticipant.score
        ).join(
            EventParticipant
        ).filter(
            EventParticipant.event_id == event_id,
            EventParticipant.score > 0
        ).order_by(
            desc(EventParticipant.score)
        ).all()
        
        scores = []
        for i, r in enumerate(results, 1):
            scores.append({
                'rank': i,
                'id': r.id,
                'name': r.name,
                'department': r.department,
                'score': r.score
            })
        
        return scores
    
    def get_department_stats(self) -> List[Dict]:
        """Get department-wise statistics"""
        results = self.db.query(
            Participant.department,
            func.count(func.distinct(Participant.id)).label('total_participants'),
            func.count(EventParticipant.event_id).label('total_participations'),
            func.avg(EventParticipant.score).label('avg_score'),
            func.sum(EventParticipant.score).label('total_score')
        ).join(
            EventParticipant, isouter=True
        ).group_by(
            Participant.department
        ).all()
        
        stats = []
        for r in results:
            stats.append({
                'department': r.department,
                'total_participants': r.total_participants,
                'total_participations': r.total_participations,
                'avg_score': float(r.avg_score or 0),
                'total_score': float(r.total_score or 0)
            })
        
        return stats