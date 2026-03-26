# backend/scripts/migrate.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run database migrations"""
    logger.info("Starting database migration...")
    
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    logger.info("Migration completed successfully!")

if __name__ == "__main__":
    run_migrations()