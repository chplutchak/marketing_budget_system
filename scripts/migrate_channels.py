"""
Migration script to populate marketing channels data
Run this once to populate your database
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.channels import MarketingChannel
from sqlalchemy.orm import Session

def get_2026_channels():
    """Return marketing channels for 2026"""
    return [
        {
            "year": 2026,
            "channel_name": "LinkedIn Organic",
            "icon": "💼",
            "color": "#0077b5",
            "frequency": "3 posts/week",
            "days": "Monday, Wednesday, Friday",
            "time_commitment": "~3 hrs/week",
            "budget": "Time only",
            "tactics": [
                "Mon: Industry insights, trends",
                "Wed: UTAK capabilities, customer stories",
                "Fri: Lighter content, team highlights"
            ],
            "order_position": 0
        },
        {
            "year": 2026,
            "channel_name": "Email Campaigns",
            "icon": "📧",
            "color": "#ea4335",
            "frequency": "1 campaign/week",
            "days": "Every Tuesday",
            "time_commitment": "~2-4 hrs/week",
            "budget": "HubSpot (included)",
            "tactics": [
                "Week 1: Educational content",
                "Week 2: Product spotlight",
                "Week 3: Customer success story",
                "Week 4: Offer/CTA"
            ],
            "order_position": 1
        },
        {
            "year": 2026,
            "channel_name": "LinkedIn Ads",
            "icon": "🎯",
            "color": "#0077b5",
            "frequency": "Always-on",
            "days": "Continuous",
            "time_commitment": "~1 hr/week",
            "budget": "$17,000/year",
            "tactics": [
                "ABM to 11 R&D targets: $12k",
                "Sponsored thought leadership: $5k",
                "Weekly monitoring & optimization"
            ],
            "order_position": 2
        },
        {
            "year": 2026,
            "channel_name": "Direct Mail",
            "icon": "📬",
            "color": "#f4b400",
            "frequency": "Quarterly",
            "days": "Month 2 of each quarter",
            "time_commitment": "~4 hrs/quarter",
            "budget": "$13,000/year",
            "tactics": [
                "Sample programs to target accounts",
                "Product announcements",
                "Personalized high-value outreach"
            ],
            "order_position": 3
        },
        {
            "year": 2026,
            "channel_name": "Conventions",
            "icon": "🎪",
            "color": "#34a853",
            "frequency": "3 per year",
            "days": "MATT (Q1), CAT (Q2), SOFT (Q3)",
            "time_commitment": "~1 week each",
            "budget": "$55,000/year",
            "tactics": [
                "Pre-event email campaigns",
                "Booth presence & demos",
                "48-hour follow-up blitz"
            ],
            "order_position": 4
        },
        {
            "year": 2026,
            "channel_name": "Website/SEO",
            "icon": "🌐",
            "color": "#4285f4",
            "frequency": "Ongoing",
            "days": "Continuous optimization",
            "time_commitment": "Vendor-managed",
            "budget": "$60,000/year",
            "tactics": [
                "CaliNetworks: SEO monitoring",
                "Product page optimization",
                "Content updates for AI search"
            ],
            "order_position": 5
        }
    ]

def migrate_channels(db: Session, year: int = 2026):
    """Migrate channels data"""
    
    print(f"Starting migration for {year} marketing channels...")
    
    # Check if data already exists
    existing = db.query(MarketingChannel).filter(MarketingChannel.year == year).first()
    
    if existing:
        print(f"  Channels for {year} already exist, skipping...")
        return 0
    
    # Create channels
    channels_data = get_2026_channels()
    for channel_data in channels_data:
        channel = MarketingChannel(**channel_data)
        db.add(channel)
    
    print(f"  ✓ Created {len(channels_data)} marketing channels")
    
    db.commit()
    
    return len(channels_data)

def main():
    """Main migration function"""
    print("=" * 60)
    print("Marketing Channels Data Migration")
    print("=" * 60)
    print()
    
    print("Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables ready")
    print()
    
    db = SessionLocal()
    
    try:
        channels_created = migrate_channels(db, year=2026)
        
        print()
        print("=" * 60)
        print("✓ Migration successful!")
        print(f"  {channels_created} channels created")
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