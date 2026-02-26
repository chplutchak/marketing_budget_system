"""
Migration script to populate strategic foundation data
Run this once to populate your database
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.strategic_foundation import StrategicTarget, TargetAudience, MarketingObjective
from sqlalchemy.orm import Session

def get_2026_targets():
    """Return strategic targets for 2026"""
    return [
        {
            "year": 2026,
            "metric_name": "Revenue Target",
            "target_value": "$7.1M",
            "delta_value": "$X.XX current",
            "order_position": 0
        },
        {
            "year": 2026,
            "metric_name": "New Leads/Month",
            "target_value": "60-80",
            "delta_value": "+10-30 vs current",
            "order_position": 1
        },
        {
            "year": 2026,
            "metric_name": "Website Conversion",
            "target_value": "2%",
            "delta_value": "+1.4% vs 0.6%",
            "order_position": 2
        },
        {
            "year": 2026,
            "metric_name": "R&D Partnerships",
            "target_value": "3 by June",
            "delta_value": "New initiative",
            "order_position": 3
        }
    ]

def get_2026_audiences():
    """Return target audiences for 2026"""
    return [
        {
            "year": 2026,
            "priority": "PRIMARY",
            "audience_name": "Clinical Labs at Large Healthcare",
            "color": "#1f77b4",
            "icon": "🥇",
            "details": {
                "Examples": "Millennium, Mayo, Quest",
                "Cycle": "6+ months",
                "Strategy": "ABM, technical content, relationship building"
            },
            "order_position": 0
        },
        {
            "year": 2026,
            "priority": "SECONDARY",
            "audience_name": "Toxicology Labs",
            "color": "#2ca02c",
            "icon": "🥈",
            "details": {
                "Type": "Independent tox labs, hospital tox",
                "Cycle": "3-6 months",
                "Strategy": "Product campaigns, sample programs"
            },
            "order_position": 1
        },
        {
            "year": 2026,
            "priority": "TERTIARY",
            "audience_name": "R&D Partnership Targets",
            "color": "#ff7f0e",
            "icon": "🥉",
            "details": {
                "Count": "11 identified organizations",
                "Cycle": "6-12 months",
                "Strategy": "Targeted outreach, capability presentations"
            },
            "order_position": 2
        },
        {
            "year": 2026,
            "priority": "ONGOING",
            "audience_name": "Existing Customers",
            "color": "#9467bd",
            "icon": "♻️",
            "details": {
                "Count": "213 active customers",
                "Value": "$7.2M portfolio",
                "Strategy": "Upsell, cross-sell, retention"
            },
            "order_position": 3
        }
    ]

def get_2026_objectives():
    """Return marketing objectives for 2026"""
    return [
        {
            "year": 2026,
            "icon": "📈",
            "title": "Lead Generation",
            "target": "60-80 new contacts/month",
            "measurement": "HubSpot tracking",
            "order_position": 0
        },
        {
            "year": 2026,
            "icon": "🎤",
            "title": "Thought Leadership",
            "target": "Consistent LinkedIn presence",
            "measurement": "Engagement metrics",
            "order_position": 1
        },
        {
            "year": 2026,
            "icon": "🚀",
            "title": "Product Launches",
            "target": "2 products ready for SOFT (Sept)",
            "measurement": "Launch metrics",
            "order_position": 2
        },
        {
            "year": 2026,
            "icon": "💻",
            "title": "Website Conversion",
            "target": "2%+ conversion rate (80+ forms/month)",
            "measurement": "GA4 tracking",
            "order_position": 3
        },
        {
            "year": 2026,
            "icon": "💼",
            "title": "LinkedIn Presence",
            "target": "3 posts/week, +500 followers",
            "measurement": "LinkedIn analytics",
            "order_position": 4
        }
    ]

def migrate_strategic_foundation(db: Session, year: int = 2026):
    """Migrate strategic foundation data"""
    
    print(f"Starting migration for {year} strategic foundation...")
    
    # Check if data already exists
    existing_targets = db.query(StrategicTarget).filter(StrategicTarget.year == year).first()
    
    if existing_targets:
        print(f"  Strategic foundation for {year} already exists, skipping...")
        return 0, 0, 0
    
    # Create targets
    targets_data = get_2026_targets()
    for target_data in targets_data:
        target = StrategicTarget(**target_data)
        db.add(target)
    
    print(f"  ✓ Created {len(targets_data)} strategic targets")
    
    # Create audiences
    audiences_data = get_2026_audiences()
    for audience_data in audiences_data:
        audience = TargetAudience(**audience_data)
        db.add(audience)
    
    print(f"  ✓ Created {len(audiences_data)} target audiences")
    
    # Create objectives
    objectives_data = get_2026_objectives()
    for objective_data in objectives_data:
        objective = MarketingObjective(**objective_data)
        db.add(objective)
    
    print(f"  ✓ Created {len(objectives_data)} marketing objectives")
    
    db.commit()
    
    return len(targets_data), len(audiences_data), len(objectives_data)

def main():
    """Main migration function"""
    print("=" * 60)
    print("Strategic Foundation Data Migration")
    print("=" * 60)
    print()
    
    print("Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables ready")
    print()
    
    db = SessionLocal()
    
    try:
        targets, audiences, objectives = migrate_strategic_foundation(db, year=2026)
        
        print()
        print("=" * 60)
        print("✓ Migration successful!")
        print(f"  {targets} targets created")
        print(f"  {audiences} audiences created")
        print(f"  {objectives} objectives created")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ Migration failed!")
        print(f"Error: {str(e)}")
        print("=" * 60)
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    main()