"""
Migration script to convert hardcoded calendar data to database records
Run this once to populate your database with the 2026 marketing calendar
"""
import sys
import os

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.marketing_calendar import MarketingCalendar, MarketingActivity
from sqlalchemy.orm import Session

def get_hardcoded_calendar_data():
    """Return the hardcoded calendar data structure"""
    return {
        1: {  # January
            "focus": "Foundation Setting",
            "major_campaigns": ["Website Launch", "New Year Customer Outreach"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Product Spotlight", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Content Planning", "friday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Direct Mail Planning", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("Product #1 Launch Prep", "thursday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False)
                ]
            }
        },
        2: {  # February
            "focus": "Product Launch #1 Execution",
            "major_campaigns": ["Product #1 Launch Campaign", "MATT Prep"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: Product #1 Launch Announcement", "monday", False),
                    ("Email: Product #1 Launch Campaign", "tuesday", False),
                    ("LinkedIn: Product #1 Features/Benefits", "wednesday", False),
                    ("LinkedIn: Team Behind Product #1", "friday", False),
                    ("Direct Mail Execution - Product #1", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: Early Product #1 Customer Story", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("MATT Materials Prep", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: MATT Preview/What to Expect", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: UTAK at MATT - Booth Info", "wednesday", False),
                    ("LinkedIn: Team Heading to MATT", "friday", False),
                    ("MATT Pre-Event Campaign Launch", "thursday", False)
                ]
            }
        },
        3: {  # March
            "focus": "MATT Convention & Q1 Close",
            "major_campaigns": ["MATT Convention", "Q1 Reporting"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Final MATT Reminder", "monday", False),
                    ("Email: Meet Us at MATT", "tuesday", False),
                    ("LinkedIn: Live Updates from MATT", "wednesday", False),
                    ("MATT Convention Days", "thursday", False),
                    ("MATT Follow-up Emails Start", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: MATT Recap & Highlights", "monday", False),
                    ("Email: Product Spotlight", "tuesday", False),
                    ("LinkedIn: MATT Key Takeaways", "wednesday", False),
                    ("LinkedIn: Thank You MATT Attendees", "friday", False),
                    ("MATT Lead Nurture Setup", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Industry Insights from MATT", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Q2 Planning Kickoff", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Q1 Wins & Learnings", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: Looking Ahead to Q2", "wednesday", False),
                    ("LinkedIn: Team Q1 Celebration", "friday", False),
                    ("Q1 Performance Report", "thursday", False)
                ]
            }
        },
        4: {  # April
            "focus": "Product #2 Development & R&D Push",
            "major_campaigns": ["Product #2 Prep", "R&D Outreach Campaign"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: R&D Partnership Value Prop", "monday", False),
                    ("Email: R&D Partnership Opportunities", "tuesday", False),
                    ("LinkedIn: UTAK R&D Capabilities", "wednesday", False),
                    ("LinkedIn: Team - R&D Focus", "friday", False),
                    ("Direct Mail Planning - R&D Targets", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: Custom-to-Stock Success Story", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Product #2 Content Development", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Sneak Peek Product #2", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: UTAK Innovation Process", "wednesday", False),
                    ("LinkedIn: Team Behind Product #2", "friday", False),
                    ("CAT Convention Prep Start", "thursday", False)
                ]
            }
        },
        5: {  # May
            "focus": "Product #2 Launch & CAT",
            "major_campaigns": ["Product #2 Launch", "CAT Prep"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: Product #2 Launch Announcement", "monday", False),
                    ("Email: Product #2 Launch Campaign", "tuesday", False),
                    ("LinkedIn: Product #2 Technical Deep Dive", "wednesday", False),
                    ("LinkedIn: Product #2 Applications", "friday", False),
                    ("Direct Mail Execution - Product #2", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Product #2 vs Alternatives", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: Both Products Together Value", "wednesday", False),
                    ("LinkedIn: Team CAT Prep", "friday", False),
                    ("CAT Materials Preparation", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: CAT Preview/Meet Us There", "monday", False),
                    ("Email: CAT Pre-Event - Meet UTAK", "tuesday", False),
                    ("LinkedIn: What We're Showcasing at CAT", "wednesday", False),
                    ("LinkedIn: Team Heading to CAT", "friday", False),
                    ("CAT Pre-Event Campaign", "thursday", False)
                ]
            }
        },
        6: {  # June
            "focus": "CAT Convention & Mid-Year Review",
            "major_campaigns": ["CAT Convention", "R&D Partnership Check-in", "Mid-Year Reporting"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Final CAT Reminder", "monday", False),
                    ("Email: Last Chance - Visit UTAK at CAT", "tuesday", False),
                    ("LinkedIn: Live from CAT", "wednesday", False),
                    ("CAT Convention Days", "thursday", False),
                    ("CAT Follow-up Emails Start", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: CAT Recap & Key Moments", "monday", False),
                    ("Email: Product Spotlight", "tuesday", False),
                    ("LinkedIn: CAT Connections & Learnings", "wednesday", False),
                    ("LinkedIn: Thank You CAT Attendees", "friday", False),
                    ("R&D Partnership Status Review", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Mid-Year Industry Trends", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: UTAK First Half Achievements", "wednesday", False),
                    ("LinkedIn: Team Mid-Year Celebration", "friday", False),
                    ("Q3 SOFT Planning Begins", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Looking Ahead to H2", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: SOFT September Preview", "wednesday", False),
                    ("LinkedIn: Team Gearing Up for SOFT", "friday", False),
                    ("Mid-Year Performance Report", "thursday", False)
                ]
            }
        },
        7: {  # July
            "focus": "SOFT Preparation Begins",
            "major_campaigns": ["SOFT Pre-Event Campaign Launch"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: SOFT September Announcement", "monday", False),
                    ("Email: SOFT Pre-Event Wave 1", "tuesday", False),
                    ("LinkedIn: Why Attend SOFT", "wednesday", False),
                    ("LinkedIn: Team SOFT Prep Begins", "friday", False),
                    ("Direct Mail Planning - SOFT Targets", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: SOFT Session Previews", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: What UTAK is Bringing to SOFT", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("SOFT Materials Design Start", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: SOFT Networking Preview", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: UTAK SOFT History/Highlights", "wednesday", False),
                    ("LinkedIn: Team Countdown to SOFT", "friday", False),
                    ("SOFT Booth Design Finalize", "thursday", False)
                ]
            }
        },
        8: {  # August
            "focus": "SOFT Final Prep",
            "major_campaigns": ["SOFT Direct Mail", "SOFT Pre-Event Intensifies"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: 30 Days to SOFT", "monday", False),
                    ("Email: SOFT Pre-Event Wave 2", "tuesday", False),
                    ("LinkedIn: UTAK Booth Location & Details", "wednesday", False),
                    ("LinkedIn: Meet the UTAK SOFT Team", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: SOFT Product Showcase Preview", "monday", False),
                    ("Email: Product Spotlight", "tuesday", False),
                    ("LinkedIn: Schedule Your SOFT Meeting", "wednesday", False),
                    ("LinkedIn: SOFT Demos & Presentations", "friday", False),
                    ("Direct Mail Execution - SOFT VIPs", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: 2 Weeks to SOFT", "monday", False),
                    ("Email: SOFT Pre-Event Wave 3", "tuesday", False),
                    ("LinkedIn: SOFT Must-See Sessions", "wednesday", False),
                    ("LinkedIn: Team Final SOFT Prep", "friday", False),
                    ("SOFT Booth Materials Complete", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Final Week - SOFT Countdown", "monday", False),
                    ("Email: Final SOFT Reminder - Visit Us", "tuesday", False),
                    ("LinkedIn: UTAK SOFT Schedule", "wednesday", False),
                    ("LinkedIn: Team Traveling to SOFT", "friday", False),
                    ("SOFT Prep Complete - Travel", "thursday", False)
                ]
            }
        },
        9: {  # September
            "focus": "SOFT/TIAFT - BIGGEST EVENT",
            "major_campaigns": ["SOFT Convention", "Product Showcase", "Aggressive Follow-up"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: SOFT This Week!", "monday", False),
                    ("Email: Last Call - Meet UTAK at SOFT", "tuesday", False),
                    ("LinkedIn: En Route to SOFT", "wednesday", False),
                    ("SOFT Setup Day", "thursday", False),
                    ("SOFT Convention Day 1", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: Live from SOFT - Day 2", "monday", False),
                    ("LinkedIn: SOFT Day 3 Highlights", "tuesday", False),
                    ("LinkedIn: SOFT Wrap-up & Thank Yous", "wednesday", False),
                    ("SOFT Travel Back", "thursday", False),
                    ("Lead Data Entry Begins", "friday", False)
                ],
                "Week 3": [
                    ("LinkedIn: SOFT Top 5 Takeaways", "monday", False),
                    ("Email: SOFT Follow-up Wave 1", "tuesday", False),
                    ("LinkedIn: SOFT Connections Recap", "wednesday", False),
                    ("LinkedIn: Thank You SOFT Attendees", "friday", False),
                    ("SOFT Follow-up Calls Start", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: SOFT Learnings Applied", "monday", False),
                    ("Email: SOFT Follow-up Wave 2", "tuesday", False),
                    ("LinkedIn: SOFT Lead Stories Begin", "wednesday", False),
                    ("LinkedIn: Team Post-SOFT Debrief", "friday", False),
                    ("Q3 Performance Report", "thursday", False)
                ]
            }
        },
        10: {  # October
            "focus": "SOFT Lead Nurture & Q4 Planning",
            "major_campaigns": ["SOFT Lead Nurture", "Q4 Campaign Planning"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: SOFT Success Story #1", "monday", False),
                    ("Email: SOFT Lead Follow-up Campaign", "tuesday", False),
                    ("LinkedIn: Implementing SOFT Insights", "wednesday", False),
                    ("LinkedIn: Team Q4 Focus", "friday", False),
                    ("Q4 Campaign Planning Workshop", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("2027 Budget Development Start", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Q4 Priorities Preview", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: Year-End Planning", "wednesday", False),
                    ("LinkedIn: Team Preparing for Year-End", "friday", False),
                    ("2027 Strategic Planning", "thursday", False)
                ]
            }
        },
        11: {  # November
            "focus": "Year-End Push & 2027 Planning",
            "major_campaigns": ["Year-End Campaign", "Customer Retention"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Educational Content", "tuesday", False),
                    ("LinkedIn: UTAK Story/Customer Success", "wednesday", False),
                    ("LinkedIn: Team Highlights/Culture", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: Year-End Planning Tips", "monday", False),
                    ("Email: Year-End Special Offer", "tuesday", False),
                    ("LinkedIn: 2026 UTAK Wins", "wednesday", False),
                    ("LinkedIn: Team Gratitude", "friday", False),
                    ("Direct Mail Planning - Year-End", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Industry Year in Review", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: Customer Appreciation", "wednesday", False),
                    ("LinkedIn: Team Year-End Reflections", "friday", False),
                    ("2027 Budget Finalization", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Getting Ready for 2027", "monday", False),
                    ("Email: Offer/CTA (Samples, Consult)", "tuesday", False),
                    ("LinkedIn: UTAK 2027 Preview", "wednesday", False),
                    ("LinkedIn: Team Holiday Prep", "friday", False),
                    ("2027 Marketing Plan Draft", "thursday", False)
                ]
            }
        },
        12: {  # December
            "focus": "Year-End & 2027 Prep",
            "major_campaigns": ["Customer Appreciation", "2027 Kickoff Planning"],
            "weekly_tasks": {
                "Week 1": [
                    ("LinkedIn: Industry Insights/Trends", "monday", False),
                    ("Email: Customer Appreciation", "tuesday", False),
                    ("LinkedIn: Thank You 2026", "wednesday", False),
                    ("LinkedIn: Team Year in Review", "friday", False),
                    ("Monthly Review", "friday", False)
                ],
                "Week 2": [
                    ("LinkedIn: 2026 Top Moments", "monday", False),
                    ("Email: Product Spotlight", "tuesday", False),
                    ("LinkedIn: Customer Stories of 2026", "wednesday", False),
                    ("LinkedIn: Team Holiday Spirit", "friday", False),
                    ("Direct Mail Execution - Appreciation", "thursday", False)
                ],
                "Week 3": [
                    ("LinkedIn: Looking Forward to 2027", "monday", False),
                    ("Email: Customer Success Story", "tuesday", False),
                    ("LinkedIn: UTAK 2027 Goals", "wednesday", False),
                    ("LinkedIn: Team Holiday Message", "friday", False),
                    ("Annual Performance Review", "thursday", False)
                ],
                "Week 4": [
                    ("LinkedIn: Happy Holidays from UTAK", "monday", False),
                    ("Email: Year-End Thank You", "tuesday", False),
                    ("LinkedIn: 2026 Thank You Message", "wednesday", False),
                    ("LinkedIn: Team 2027 Kickoff Preview", "friday", False),
                    ("2026 Annual Report Complete", "thursday", False)
                ]
            }
        }
    }


def migrate_calendar_to_database(db: Session, year: int = 2026):
    """Migrate hardcoded calendar data to database"""
    
    monthly_activities = get_hardcoded_calendar_data()
    
    print(f"Starting migration for {year} marketing calendar...")
    print(f"Found {len(monthly_activities)} months to migrate")
    
    total_calendars = 0
    total_activities = 0
    
    for month, data in monthly_activities.items():
        # Check if calendar already exists
        existing = db.query(MarketingCalendar).filter(
            MarketingCalendar.year == year,
            MarketingCalendar.month == month
        ).first()
        
        if existing:
            print(f"  Month {month}: Already exists, skipping...")
            continue
        
        # Create calendar entry
        calendar = MarketingCalendar(
            year=year,
            month=month,
            focus=data.get("focus"),
            major_campaigns=data.get("major_campaigns", [])
        )
        
        db.add(calendar)
        db.flush()  # Get the ID without committing
        
        total_calendars += 1
        
        # Create activities for this calendar
        week_activities = data.get("weekly_tasks", {})
        
        for week_name, tasks in week_activities.items():
            # Extract week number from "Week 1", "Week 2", etc.
            week_num = int(week_name.split()[1])
            
            for order, (task_name, day, completed) in enumerate(tasks):
                activity = MarketingActivity(
                    calendar_id=calendar.id,
                    week_number=week_num,
                    activity_name=task_name,
                    day_of_week=day,
                    order_in_week=order,
                    is_completed=completed
                )
                db.add(activity)
                total_activities += 1
        
        print(f"  Month {month}: Created calendar with {len(week_activities) * 5} activities")
    
    # Commit all changes
    db.commit()
    
    print(f"\nMigration complete!")
    print(f"  Created {total_calendars} calendars")
    print(f"  Created {total_activities} activities")
    
    return total_calendars, total_activities


def main():
    """Main migration function"""
    print("=" * 60)
    print("Marketing Calendar Data Migration")
    print("=" * 60)
    print()
    
    # Create tables if they don't exist
    print("Ensuring database tables exist...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables ready")
    print()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Run migration
        calendars_created, activities_created = migrate_calendar_to_database(db, year=2026)
        
        print()
        print("=" * 60)
        print("✓ Migration successful!")
        print(f"  {calendars_created} calendars created")
        print(f"  {activities_created} activities created")
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