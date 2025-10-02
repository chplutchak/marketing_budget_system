from fastapi import FastAPI
from sqlalchemy import text
import sys
import os

# Add the current directory to Python path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.config import settings
from app.database import engine, SessionLocal

# Create database tables
from app.database import Base
from app.models.campaign import Campaign
from app.models.budget import BudgetItem
from app.models.expense import ActualExpense
from app.models.roi import ROIMetric
from app.models.cost_center import CostCenter

Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    debug=settings.debug
)

# Import and include routers
try:
    from app.api.endpoints.campaigns import router as campaigns_router
    from app.api.endpoints.budgets import router as budgets_router
    from app.api.endpoints.cost_centers import router as cost_centers_router
    from app.api.endpoints.expenses import router as expenses_router
    from app.api.endpoints.roi import router as roi_router
    
    app.include_router(campaigns_router, prefix="/api/campaigns", tags=["campaigns"])
    app.include_router(budgets_router, prefix="/api/budgets", tags=["budget-items"])
    app.include_router(cost_centers_router, prefix="/api/cost-centers", tags=["cost-centers"])
    app.include_router(expenses_router, prefix="/api/expenses", tags=["expenses"])
    app.include_router(roi_router, prefix="/api/roi", tags=["roi-metrics"])
    
except ImportError as e:
    print(f"Warning: Could not import some routers - {e}")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Marketing Budget Management System API",
        "version": settings.app_version,
        "status": "healthy"
    }

# Health check for database
@app.get("/health")
async def health_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)