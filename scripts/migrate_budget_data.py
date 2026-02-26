"""
Migration script to populate 2026 marketing budget data
Run this once to populate your database with budget information
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.marketing_budget import MarketingBudget, BudgetCategory
from sqlalchemy.orm import Session

def get_2026_budget_data():
    """Return the 2026 budget structure"""
    return {
        "year": 2026,
        "total_budget": 213000,
        "fixed_costs": 115232,
        "flexible_budget": 97768,
        "fixed_costs_detail": {
            "CaliNetworks": 24450,
            "Conventions": 40711,
            "HubSpot": 26875,
            "Designer": 23196
        },
        "flexible_budget_detail": {
            "Convention Support": 30000,
            "R&D / Direct Mail": 30000,
            "Content Production": 20000,
            "LinkedIn Ads": 11768,
            "Tools/Software": 3000,
            "Buffer": 3000
        },
        "quarterly_distribution": {
            "Q1": {
                "total": 48300,
                "color": "#1f77b4",
                "focus": "Website launch, Product #1, MATT"
            },
            "Q2": {
                "total": 51300,
                "color": "#ff7f0e",
                "focus": "Product #2, CAT, R&D push"
            },
            "Q3": {
                "total": 58300,
                "color": "#2ca02c",
                "focus": "SOFT prep & execution (heaviest)"
            },
            "Q4": {
                "total": 42100,
                "color": "#d62728",
                "focus": "SOFT follow-up, nurture, planning"
            }
        }
    }

def get_2026_categories():
    """Return detailed budget categories with colors and breakdowns"""
    return [
        # Fixed Costs
        {
            "category_type": "fixed",
            "category_name": "CaliNetworks",
            "amount": 24450,
            "color": "#1f77b4",
            "description": "SEO + Content",
            "breakdown": None
        },
        {
            "category_type": "fixed",
            "category_name": "Conventions",
            "amount": 40711,
            "color": "#1f77b4",
            "description": "MATT, CAT, SOFT",
            "breakdown": None
        },
        {
            "category_type": "fixed",
            "category_name": "HubSpot",
            "amount": 26875,
            "color": "#1f77b4",
            "description": "CRM + Marketing",
            "breakdown": None
        },
        {
            "category_type": "fixed",
            "category_name": "Designer",
            "amount": 23196,
            "color": "#1f77b4",
            "description": "All creative",
            "breakdown": None
        },
        # Flexible Budget
        {
            "category_type": "flexible",
            "category_name": "Convention Support",
            "amount": 30000,
            "color": "#ff7f0e",
            "description": "Materials and campaigns",
            "breakdown": {
                "Materials": 25000,
                "Pre/post campaigns": 5000
            }
        },
        {
            "category_type": "flexible",
            "category_name": "R&D / Direct Mail",
            "amount": 30000,
            "color": "#d62728",
            "description": "Sample programs and mailers",
            "breakdown": {
                "Sample programs": 15000,
                "Account mailers": 5000
            }
        },
        {
            "category_type": "flexible",
            "category_name": "Content Production",
            "amount": 20000,
            "color": "#1f77b4",
            "description": "All content creation",
            "breakdown": {
                "Copywriting": 8000,
                "Technical writing": 6000,
                "Photo/video": 4000,
                "Stock assets": 2000
            }
        },
        {
            "category_type": "flexible",
            "category_name": "LinkedIn Ads",
            "amount": 11768,
            "color": "#2ca02c",
            "description": "Paid campaigns",
            "breakdown": {
                "ABM campaigns": 5884,
                "Sponsored content": 5884
            }
        },
        {
            "category_type": "flexible",
            "category_name": "Tools/Software",
            "amount": 3000,
            "color": "#7f7f7f",
            "description": "Various sales tools",
            "breakdown": None
        },
        {
            "category_type": "flexible",
            "category_name": "Buffer",
            "amount": 3000,
            "color": "#bcbd22",
            "description": "Contingency for opportunities",
            "breakdown": None
        }
    ]

def migrate_budget_to_database(db: Session, year: int = 2026):
    """Migrate budget data to database"""
    
    print(f"Starting migration for {year} marketing budget...")
    
    # Check if budget already exists
    existing = db.query(MarketingBudget).filter(MarketingBudget.year == year).first()
    
    if existing:
        print(f"  Budget for {year} already exists, skipping...")
        return 0, 0
    
    # Get budget data
    budget_data = get_2026_budget_data()
    
    # Create budget entry
    budget = MarketingBudget(**budget_data)
    db.add(budget)
    db.flush()  # Get the ID without committing
    
    print(f"  ✓ Created main budget record")
    
    # Create categories
    categories_data = get_2026_categories()
    category_count = 0
    
    for cat_data in categories_data:
        category = BudgetCategory(
            budget_id=budget.id,
            year=year,
            **cat_data
        )
        db.add(category)
        category_count += 1
    
    print(f"  ✓ Created {category_count} budget categories")
    
    # Commit all changes
    db.commit()
    
    return 1, category_count

def main():
    """Main migration function"""
    print("=" * 60)
    print("Marketing Budget Data Migration")
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
        budgets_created, categories_created = migrate_budget_to_database(db, year=2026)
        
        print()
        print("=" * 60)
        print("✓ Migration successful!")
        print(f"  {budgets_created} budget created")
        print(f"  {categories_created} categories created")
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