# backend/app/services/venue_service.py
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import uuid
import logging

from app.models import Venue, VenueBooking, Event
from app.services.email_service import email_service

logger = logging.getLogger(__name__)

class VenueService:
    def __init__(self, db: Session):
        self.db = db
    
    def check_availability(
        self,
        venue_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """Check if venue is available for given time slot"""
        conflicting = self.db.query(VenueBooking).filter(
            VenueBooking.venue_id == venue_id,
            VenueBooking.status.in_(['pending', 'confirmed']),
            VenueBooking.start_time < end_time,
            VenueBooking.end_time > start_time
        ).first()
        
        return conflicting is None
    
    def get_available_venues(
        self,
        start_time: datetime,
        end_time: datetime,
        min_capacity: int = 0,
        requirements: dict = None
    ) -> List[Venue]:
        """Get all available venues for time slot"""
        # Get all active venues meeting capacity
        query = self.db.query(Venue).filter(
            Venue.is_active == True,
            Venue.capacity >= min_capacity
        )
        
        # Apply requirements
        if requirements:
            if requirements.get('projector'):
                query = query.filter(Venue.has_projector == True)
            if requirements.get('sound_system'):
                query = query.filter(Venue.has_sound_system == True)
            if requirements.get('ac'):
                query = query.filter(Venue.has_ac == True)
        
        venues = query.all()
        
        # Filter by availability
        available = []
        for venue in venues:
            if self.check_availability(venue.id, start_time, end_time):
                available.append(venue)
        
        return available
    
    def book_venue(
        self,
        venue_id: int,
        event_id: int,
        start_time: datetime,
        end_time: datetime,
        booked_by: int,
        requirements: dict = None
    ) -> Optional[VenueBooking]:
        """Create a new venue booking"""
        # Check availability
        if not self.check_availability(venue_id, start_time, end_time):
            logger.warning(f"Venue {venue_id} not available")
            return None
        
        # Generate booking reference
        booking_ref = f"VB{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        
        # Create booking
        booking = VenueBooking(
            venue_id=venue_id,
            event_id=event_id,
            booking_reference=booking_ref,
            start_time=start_time,
            end_time=end_time,
            booked_by=booked_by,
            status='pending'
        )
        
        self.db.add(booking)
        self.db.flush()
        
        # Update event status
        event = self.db.query(Event).get(event_id)
        if event:
            event.status = 'venue_confirmed'
        
        self.db.commit()
        self.db.refresh(booking)
        
        # Send notification
        venue = self.db.query(Venue).get(venue_id)
        email_service.send_venue_booking_notification(
            event=event,
            venue_name=venue.name,
            start_time=start_time,
            end_time=end_time
        )
        
        logger.info(f"Booking created: {booking_ref}")
        return booking
    
    def confirm_booking(self, booking_id: int, confirmed_by: int) -> bool:
        """Confirm a booking"""
        booking = self.db.query(VenueBooking).get(booking_id)
        if not booking or booking.status != 'pending':
            return False
        
        booking.status = 'confirmed'
        booking.confirmed_by = confirmed_by
        booking.confirmation_date = datetime.now()
        
        self.db.commit()
        return True
    
    def cancel_booking(self, booking_id: int, reason: str = None) -> bool:
        """Cancel a booking"""
        booking = self.db.query(VenueBooking).get(booking_id)
        if not booking:
            return False
        
        booking.status = 'cancelled'
        booking.notes = reason
        
        # Update event status
        event = self.db.query(Event).get(booking.event_id)
        if event and event.status == 'venue_confirmed':
            event.status = 'planned'
        
        self.db.commit()
        return True