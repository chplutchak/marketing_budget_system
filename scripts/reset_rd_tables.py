"""
Script to drop and recreate R&D tables with updated schema
WARNING: This will delete all existing R&D data!
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import SessionLocal, engine, Base

# Import all R&D models so Base.metadata knows about them
from app.models.rd_initiative import (
    RDInitiative,
    RDInitiativeTeam,
    RDFeasibility,
    RDCustomerInterest,
    RDSample,
    RDContact,
    RDMilestone,
    RDROI,
    RDExpense,
    RDRevenue,
    RDNote,
)

# Drop order matters — child tables (with FKs) must be dropped before parents
TABLES_TO_DROP = [
    "rd_notes",
    "rd_revenue",
    "rd_expenses",
    "rd_roi",
    "rd_milestones",
    "rd_contacts",
    "rd_samples",
    "rd_customer_interest",
    "rd_feasibility",
    "rd_initiative_team",
    "rd_initiatives",
    # Legacy table names (in case they exist from older schema)
    "rd_notes_old",
    "feasibility_checks",
    "manufacturing_info",
    "sample_tracking",
    "customer_interests",
]


def reset_rd_tables():
    print("=" * 60)
    print("R&D Tables Reset")
    print("=" * 60)
    print()

    db = SessionLocal()

    try:
        print("Dropping old R&D tables...")
        for table in TABLES_TO_DROP:
            try:
                db.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                print(f"  ✓ Dropped {table}")
            except Exception as e:
                print(f"  - Skipped {table}: {e}")

        db.commit()
        print()

        print("Creating tables with new schema...")
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created")
        print()

        # Verify tables were created
        print("Verifying tables...")
        expected_tables = [
            "rd_initiatives",
            "rd_initiative_team",
            "rd_feasibility",
            "rd_customer_interest",
            "rd_samples",
            "rd_contacts",
            "rd_milestones",
            "rd_roi",
            "rd_expenses",
            "rd_revenue",
            "rd_notes",
        ]
        for table in expected_tables:
            result = db.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
            ).scalar()
            status = "✓" if result else "✗ MISSING"
            print(f"  {status} {table}")

        print()
        print("=" * 60)
        print("✓ Reset complete! R&D tables reflect the latest schema.")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print()
    print("⚠️  WARNING: This will delete all existing R&D initiative data!")
    print()

    if sys.stdin.isatty():
        response = input("Type 'YES' to continue: ")
        if response != "YES":
            print("Cancelled.")
            sys.exit(0)
    else:
        print("Running in non-interactive mode — proceeding automatically...")
        print()

    reset_rd_tables()