"""
Script to drop and recreate R&D tables with updated schema
WARNING: This will delete all existing R&D data!
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.rd_initiative import RDInitiative, CustomerInterest, SampleTracking, ManufacturingInfo, FeasibilityCheck

def reset_rd_tables():
    """Drop and recreate R&D tables"""
    
    print("=" * 60)
    print("R&D Tables Reset")
    print("=" * 60)
    print()
    
    # Drop tables
    print("Dropping old R&D tables...")
    RDInitiative.__table__.drop(engine, checkfirst=True)
    CustomerInterest.__table__.drop(engine, checkfirst=True)
    SampleTracking.__table__.drop(engine, checkfirst=True)
    ManufacturingInfo.__table__.drop(engine, checkfirst=True)
    FeasibilityCheck.__table__.drop(engine, checkfirst=True)
    print("✓ Old tables dropped")
    print()
    
    # Recreate with new schema
    print("Creating tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created with updated schema")
    print()
    
    print("=" * 60)
    print("✓ Reset complete!")
    print("R&D tables now have the latest schema")
    print("=" * 60)

if __name__ == "__main__":
    import warnings
    
    print()
    print("⚠️  WARNING: This will delete all existing R&D initiative data!")
    print()
    response = input("Type 'YES' to continue: ")
    
    if response == "YES":
        reset_rd_tables()
    else:
        print("Cancelled.")