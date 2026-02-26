from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.rd_initiative import RDInitiative, RDInitiativeCreate, RDInitiativeUpdate, RDInitiativeDetail
from app.schemas.rd_feasibility import RDFeasibility, RDFeasibilityCreate, RDFeasibilityUpdate
from app.schemas.rd_customer_interest import RDCustomerInterest, RDCustomerInterestCreate, RDCustomerInterestUpdate
from app.schemas.rd_sample import RDSample, RDSampleCreate, RDSampleUpdate
from app.schemas.rd_contact import RDContact, RDContactCreate, RDContactUpdate
from app.schemas.rd_milestone import RDMilestone, RDMilestoneCreate, RDMilestoneUpdate
from app.schemas.rd_expense import RDExpense, RDExpenseCreate, RDExpenseUpdate
from app.schemas.rd_revenue import RDRevenue, RDRevenueCreate, RDRevenueUpdate
from app.schemas.rd_note import RDNote, RDNoteCreate, RDNoteUpdate
from app.schemas.rd_roi import RDROI, RDROICreate, RDROIUpdate
from app.schemas.rd_team import RDInitiativeTeam, RDInitiativeTeamCreate, RDInitiativeTeamUpdate

from app.crud import (
    rd_initiative,
    rd_feasibility,
    rd_customer_interest,
    rd_sample,
    rd_contact,
    rd_milestone,
    rd_expense,
    rd_revenue,
    rd_note,
    rd_roi,
    rd_team
)

router = APIRouter()


# ===========================
# INITIATIVES (Main Projects)
# ===========================

@router.get("/initiatives", response_model=List[RDInitiative])
def get_initiatives(
    skip: int = 0,
    limit: int = 100,
    stage: Optional[str] = None,
    priority: Optional[str] = None,
    is_active: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all R&D initiatives with optional filters"""
    initiatives = rd_initiative.get_initiatives(
        db, skip=skip, limit=limit, stage=stage, priority=priority, is_active=is_active
    )
    return initiatives


@router.get("/initiatives/{initiative_id}", response_model=RDInitiativeDetail)
def get_initiative(initiative_id: int, db: Session = Depends(get_db)):
    """Get a specific R&D initiative with all related data"""
    initiative = rd_initiative.get_initiative_with_details(db, initiative_id=initiative_id)
    if not initiative:
        raise HTTPException(status_code=404, detail="R&D initiative not found")
    return initiative


@router.post("/initiatives", response_model=RDInitiative)
def create_initiative(initiative: RDInitiativeCreate, db: Session = Depends(get_db)):
    """Create a new R&D initiative"""
    return rd_initiative.create_initiative(db=db, initiative=initiative)


@router.put("/initiatives/{initiative_id}", response_model=RDInitiative)
def update_initiative(
    initiative_id: int,
    initiative: RDInitiativeUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing R&D initiative"""
    db_initiative = rd_initiative.update_initiative(db, initiative_id=initiative_id, initiative=initiative)
    if not db_initiative:
        raise HTTPException(status_code=404, detail="R&D initiative not found")
    return db_initiative


@router.delete("/initiatives/{initiative_id}")
def delete_initiative(initiative_id: int, db: Session = Depends(get_db)):
    """Delete an R&D initiative"""
    success = rd_initiative.delete_initiative(db, initiative_id=initiative_id)
    if not success:
        raise HTTPException(status_code=404, detail="R&D initiative not found")
    return {"message": "R&D initiative deleted successfully"}

# ===========================
# TEAM
# ===========================

@router.get("/initiatives/{initiative_id}/team", response_model=List[RDInitiativeTeam])
def get_initiative_team(initiative_id: int, db: Session = Depends(get_db)):
    """Get all team members for an initiative"""
    team_members = rd_team.get_team_members_by_initiative(db, initiative_id)
    return team_members


@router.get("/initiatives/{initiative_id}/team/department/{department}", response_model=List[RDInitiativeTeam])
def get_initiative_team_by_department(initiative_id: int, department: str, db: Session = Depends(get_db)):
    """Get team members for an initiative filtered by department"""
    team_members = rd_team.get_team_members_by_department(db, initiative_id, department)
    return team_members


@router.post("/initiatives/{initiative_id}/team", response_model=RDInitiativeTeam)
def add_team_member(initiative_id: int, team_member: RDInitiativeTeamCreate, db: Session = Depends(get_db)):
    """Add a team member to an initiative"""
    # Verify initiative_id matches
    if team_member.initiative_id != initiative_id:
        raise HTTPException(status_code=400, detail="Initiative ID mismatch")
    
    return rd_team.create_team_member(db, team_member)


@router.put("/team/{team_member_id}", response_model=RDInitiativeTeam)
def update_team_member(team_member_id: int, team_member: RDInitiativeTeamUpdate, db: Session = Depends(get_db)):
    """Update a team member assignment"""
    updated = rd_team.update_team_member(db, team_member_id, team_member)
    if not updated:
        raise HTTPException(status_code=404, detail="Team member not found")
    return updated


@router.delete("/team/{team_member_id}")
def remove_team_member(team_member_id: int, db: Session = Depends(get_db)):
    """Remove a team member from an initiative"""
    deleted = rd_team.delete_team_member(db, team_member_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Team member not found")
    return {"message": "Team member removed successfully"}

# ===========================
# FEASIBILITY (Manufacturing)
# ===========================

@router.get("/feasibility/initiative/{initiative_id}", response_model=RDFeasibility)
def get_feasibility_by_initiative(initiative_id: int, db: Session = Depends(get_db)):
    """Get feasibility assessment for a specific initiative"""
    feasibility = rd_feasibility.get_feasibility_by_initiative(db, initiative_id=initiative_id)
    if not feasibility:
        raise HTTPException(status_code=404, detail="Feasibility assessment not found")
    return feasibility


@router.get("/feasibility/{feasibility_id}", response_model=RDFeasibility)
def get_feasibility(feasibility_id: int, db: Session = Depends(get_db)):
    """Get a specific feasibility assessment"""
    feasibility = rd_feasibility.get_feasibility(db, feasibility_id=feasibility_id)
    if not feasibility:
        raise HTTPException(status_code=404, detail="Feasibility assessment not found")
    return feasibility


@router.post("/feasibility", response_model=RDFeasibility)
def create_feasibility(feasibility: RDFeasibilityCreate, db: Session = Depends(get_db)):
    """Create a new feasibility assessment"""
    return rd_feasibility.create_feasibility(db=db, feasibility=feasibility)


@router.put("/feasibility/{feasibility_id}", response_model=RDFeasibility)
def update_feasibility(
    feasibility_id: int,
    feasibility: RDFeasibilityUpdate,
    db: Session = Depends(get_db)
):
    """Update feasibility assessment"""
    db_feasibility = rd_feasibility.update_feasibility(db, feasibility_id=feasibility_id, feasibility=feasibility)
    if not db_feasibility:
        raise HTTPException(status_code=404, detail="Feasibility assessment not found")
    return db_feasibility


@router.delete("/feasibility/{feasibility_id}")
def delete_feasibility(feasibility_id: int, db: Session = Depends(get_db)):
    """Delete feasibility assessment"""
    success = rd_feasibility.delete_feasibility(db, feasibility_id=feasibility_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feasibility assessment not found")
    return {"message": "Feasibility assessment deleted successfully"}


# ===========================
# CUSTOMER INTEREST
# ===========================

@router.get("/customers/initiative/{initiative_id}", response_model=List[RDCustomerInterest])
def get_customers_by_initiative(
    initiative_id: int,
    interest_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all customer interest records for an initiative"""
    customers = rd_customer_interest.get_customers_by_initiative(
        db, initiative_id=initiative_id, interest_level=interest_level
    )
    return customers


@router.get("/customers/{interest_id}", response_model=RDCustomerInterest)
def get_customer_interest(interest_id: int, db: Session = Depends(get_db)):
    """Get a specific customer interest record"""
    interest = rd_customer_interest.get_customer_interest(db, interest_id=interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Customer interest record not found")
    return interest


@router.post("/customers", response_model=RDCustomerInterest)
def create_customer_interest(interest: RDCustomerInterestCreate, db: Session = Depends(get_db)):
    """Create a new customer interest record"""
    return rd_customer_interest.create_customer_interest(db=db, interest=interest)


@router.put("/customers/{interest_id}", response_model=RDCustomerInterest)
def update_customer_interest(
    interest_id: int,
    interest: RDCustomerInterestUpdate,
    db: Session = Depends(get_db)
):
    """Update customer interest record"""
    db_interest = rd_customer_interest.update_customer_interest(db, interest_id=interest_id, interest=interest)
    if not db_interest:
        raise HTTPException(status_code=404, detail="Customer interest record not found")
    return db_interest


@router.delete("/customers/{interest_id}")
def delete_customer_interest(interest_id: int, db: Session = Depends(get_db)):
    """Delete customer interest record"""
    success = rd_customer_interest.delete_customer_interest(db, interest_id=interest_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer interest record not found")
    return {"message": "Customer interest record deleted successfully"}


# ===========================
# SAMPLES
# ===========================

@router.get("/samples/initiative/{initiative_id}", response_model=List[RDSample])
def get_samples_by_initiative(initiative_id: int, db: Session = Depends(get_db)):
    """Get all samples for an initiative"""
    samples = rd_sample.get_samples_by_initiative(db, initiative_id=initiative_id)
    return samples


@router.get("/samples/converted/{initiative_id}", response_model=List[RDSample])
def get_converted_samples(initiative_id: int, db: Session = Depends(get_db)):
    """Get samples that resulted in orders for an initiative"""
    samples = rd_sample.get_converted_samples(db, initiative_id=initiative_id)
    return samples


@router.get("/samples/{sample_id}", response_model=RDSample)
def get_sample(sample_id: int, db: Session = Depends(get_db)):
    """Get a specific sample record"""
    sample = rd_sample.get_sample(db, sample_id=sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample record not found")
    return sample


@router.post("/samples", response_model=RDSample)
def create_sample(sample: RDSampleCreate, db: Session = Depends(get_db)):
    """Create a new sample record"""
    return rd_sample.create_sample(db=db, sample=sample)


@router.put("/samples/{sample_id}", response_model=RDSample)
def update_sample(
    sample_id: int,
    sample: RDSampleUpdate,
    db: Session = Depends(get_db)
):
    """Update sample record"""
    db_sample = rd_sample.update_sample(db, sample_id=sample_id, sample=sample)
    if not db_sample:
        raise HTTPException(status_code=404, detail="Sample record not found")
    return db_sample


@router.delete("/samples/{sample_id}")
def delete_sample(sample_id: int, db: Session = Depends(get_db)):
    """Delete sample record"""
    success = rd_sample.delete_sample(db, sample_id=sample_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sample record not found")
    return {"message": "Sample record deleted successfully"}


# ===========================
# CONTACTS
# ===========================

@router.get("/contacts/initiative/{initiative_id}", response_model=List[RDContact])
def get_contacts_by_initiative(
    initiative_id: int,
    contact_type: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all contact records for an initiative"""
    contacts = rd_contact.get_contacts_by_initiative(
        db, initiative_id=initiative_id, contact_type=contact_type, department=department
    )
    return contacts


@router.get("/contacts/{contact_id}", response_model=RDContact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Get a specific contact record"""
    contact = rd_contact.get_contact(db, contact_id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact record not found")
    return contact


@router.post("/contacts", response_model=RDContact)
def create_contact(contact: RDContactCreate, db: Session = Depends(get_db)):
    """Create a new contact record"""
    return rd_contact.create_contact(db=db, contact=contact)


@router.put("/contacts/{contact_id}", response_model=RDContact)
def update_contact(
    contact_id: int,
    contact: RDContactUpdate,
    db: Session = Depends(get_db)
):
    """Update contact record"""
    db_contact = rd_contact.update_contact(db, contact_id=contact_id, contact=contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact record not found")
    return db_contact


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete contact record"""
    success = rd_contact.delete_contact(db, contact_id=contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact record not found")
    return {"message": "Contact record deleted successfully"}


# ===========================
# MILESTONES
# ===========================

@router.get("/milestones/initiative/{initiative_id}", response_model=List[RDMilestone])
def get_milestones_by_initiative(
    initiative_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all milestones for an initiative"""
    milestones = rd_milestone.get_milestones_by_initiative(
        db, initiative_id=initiative_id, status=status
    )
    return milestones


@router.get("/milestones/{milestone_id}", response_model=RDMilestone)
def get_milestone(milestone_id: int, db: Session = Depends(get_db)):
    """Get a specific milestone"""
    milestone = rd_milestone.get_milestone(db, milestone_id=milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone


@router.post("/milestones", response_model=RDMilestone)
def create_milestone(milestone: RDMilestoneCreate, db: Session = Depends(get_db)):
    """Create a new milestone"""
    return rd_milestone.create_milestone(db=db, milestone=milestone)


@router.put("/milestones/{milestone_id}", response_model=RDMilestone)
def update_milestone(
    milestone_id: int,
    milestone: RDMilestoneUpdate,
    db: Session = Depends(get_db)
):
    """Update milestone"""
    db_milestone = rd_milestone.update_milestone(db, milestone_id=milestone_id, milestone=milestone)
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return db_milestone


@router.delete("/milestones/{milestone_id}")
def delete_milestone(milestone_id: int, db: Session = Depends(get_db)):
    """Delete milestone"""
    success = rd_milestone.delete_milestone(db, milestone_id=milestone_id)
    if not success:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return {"message": "Milestone deleted successfully"}


# ===========================
# EXPENSES
# ===========================

@router.get("/expenses/initiative/{initiative_id}", response_model=List[RDExpense])
def get_expenses_by_initiative(
    initiative_id: int,
    category: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all expenses for an initiative with optional filters"""
    expenses = rd_expense.get_expenses_by_initiative(
        db, initiative_id=initiative_id, category=category, department=department
    )
    return expenses


@router.get("/expenses/initiative/{initiative_id}/total")
def get_total_expenses(initiative_id: int, db: Session = Depends(get_db)):
    """Get total expenses for an initiative"""
    total = rd_expense.get_total_expenses(db, initiative_id=initiative_id)
    return {"initiative_id": initiative_id, "total_expenses": total}


@router.get("/expenses/{expense_id}", response_model=RDExpense)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Get a specific expense"""
    expense = rd_expense.get_expense(db, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("/expenses", response_model=RDExpense)
def create_expense(expense: RDExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    return rd_expense.create_expense(db=db, expense=expense)


@router.put("/expenses/{expense_id}", response_model=RDExpense)
def update_expense(
    expense_id: int,
    expense: RDExpenseUpdate,
    db: Session = Depends(get_db)
):
    """Update expense"""
    db_expense = rd_expense.update_expense(db, expense_id=expense_id, expense=expense)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete expense"""
    success = rd_expense.delete_expense(db, expense_id=expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}


# ===========================
# REVENUE
# ===========================

@router.get("/revenue/initiative/{initiative_id}", response_model=List[RDRevenue])
def get_revenue_by_initiative(initiative_id: int, db: Session = Depends(get_db)):
    """Get all revenue for an initiative"""
    revenue = rd_revenue.get_revenue_by_initiative(db, initiative_id=initiative_id)
    return revenue


@router.get("/revenue/initiative/{initiative_id}/total")
def get_total_revenue(initiative_id: int, db: Session = Depends(get_db)):
    """Get total revenue for an initiative"""
    total = rd_revenue.get_total_revenue(db, initiative_id=initiative_id)
    return {"initiative_id": initiative_id, "total_revenue": total}


@router.get("/revenue/{revenue_id}", response_model=RDRevenue)
def get_revenue(revenue_id: int, db: Session = Depends(get_db)):
    """Get a specific revenue record"""
    revenue = rd_revenue.get_revenue(db, revenue_id=revenue_id)
    if not revenue:
        raise HTTPException(status_code=404, detail="Revenue record not found")
    return revenue


@router.post("/revenue", response_model=RDRevenue)
def create_revenue(revenue: RDRevenueCreate, db: Session = Depends(get_db)):
    """Create a new revenue record"""
    return rd_revenue.create_revenue(db=db, revenue=revenue)


@router.put("/revenue/{revenue_id}", response_model=RDRevenue)
def update_revenue(
    revenue_id: int,
    revenue: RDRevenueUpdate,
    db: Session = Depends(get_db)
):
    """Update revenue record"""
    db_revenue = rd_revenue.update_revenue(db, revenue_id=revenue_id, revenue=revenue)
    if not db_revenue:
        raise HTTPException(status_code=404, detail="Revenue record not found")
    return db_revenue


@router.delete("/revenue/{revenue_id}")
def delete_revenue(revenue_id: int, db: Session = Depends(get_db)):
    """Delete revenue record"""
    success = rd_revenue.delete_revenue(db, revenue_id=revenue_id)
    if not success:
        raise HTTPException(status_code=404, detail="Revenue record not found")
    return {"message": "Revenue record deleted successfully"}


# ===========================
# NOTES
# ===========================

@router.get("/notes/initiative/{initiative_id}", response_model=List[RDNote])
def get_notes_by_initiative(
    initiative_id: int,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all notes for an initiative"""
    notes = rd_note.get_notes_by_initiative(
        db, initiative_id=initiative_id, department=department
    )
    return notes


@router.get("/notes/{note_id}", response_model=RDNote)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a specific note"""
    note = rd_note.get_note(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/notes", response_model=RDNote)
def create_note(note: RDNoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    return rd_note.create_note(db=db, note=note)


@router.put("/notes/{note_id}", response_model=RDNote)
def update_note(
    note_id: int,
    note: RDNoteUpdate,
    db: Session = Depends(get_db)
):
    """Update note"""
    db_note = rd_note.update_note(db, note_id=note_id, note=note)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete note"""
    success = rd_note.delete_note(db, note_id=note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}


# ===========================
# ROI
# ===========================

@router.get("/roi/initiative/{initiative_id}", response_model=RDROI)
def get_roi_by_initiative(initiative_id: int, db: Session = Depends(get_db)):
    """Get ROI data for a specific initiative"""
    roi = rd_roi.get_roi_by_initiative(db, initiative_id=initiative_id)
    if not roi:
        raise HTTPException(status_code=404, detail="ROI data not found")
    return roi


@router.get("/roi/{roi_id}", response_model=RDROI)
def get_roi(roi_id: int, db: Session = Depends(get_db)):
    """Get a specific ROI record"""
    roi = rd_roi.get_roi(db, roi_id=roi_id)
    if not roi:
        raise HTTPException(status_code=404, detail="ROI record not found")
    return roi


@router.post("/roi", response_model=RDROI)
def create_roi(roi: RDROICreate, db: Session = Depends(get_db)):
    """Create a new ROI record"""
    return rd_roi.create_roi(db=db, roi=roi)


@router.put("/roi/{roi_id}", response_model=RDROI)
def update_roi(
    roi_id: int,
    roi: RDROIUpdate,
    db: Session = Depends(get_db)
):
    """Update ROI record"""
    db_roi = rd_roi.update_roi(db, roi_id=roi_id, roi=roi)
    if not db_roi:
        raise HTTPException(status_code=404, detail="ROI record not found")
    return db_roi


@router.delete("/roi/{roi_id}")
def delete_roi(roi_id: int, db: Session = Depends(get_db)):
    """Delete ROI record"""
    success = rd_roi.delete_roi(db, roi_id=roi_id)
    if not success:
        raise HTTPException(status_code=404, detail="ROI record not found")
    return {"message": "ROI record deleted successfully"}
    