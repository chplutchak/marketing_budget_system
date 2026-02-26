"""
Create this new file: app/crud/rd_team.py
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDInitiativeTeam
from app.schemas.rd_team import RDInitiativeTeamCreate, RDInitiativeTeamUpdate


def get_team_member(db: Session, team_member_id: int) -> Optional[RDInitiativeTeam]:
    """Get a single team member by ID"""
    return db.query(RDInitiativeTeam).filter(RDInitiativeTeam.id == team_member_id).first()


def get_team_members_by_initiative(db: Session, initiative_id: int) -> List[RDInitiativeTeam]:
    """Get all team members for an initiative"""
    return db.query(RDInitiativeTeam).filter(
        RDInitiativeTeam.initiative_id == initiative_id
    ).order_by(RDInitiativeTeam.department).all()


def get_team_members_by_department(db: Session, initiative_id: int, department: str) -> List[RDInitiativeTeam]:
    """Get team members for an initiative filtered by department"""
    return db.query(RDInitiativeTeam).filter(
        RDInitiativeTeam.initiative_id == initiative_id,
        RDInitiativeTeam.department == department
    ).all()


def create_team_member(db: Session, team_member: RDInitiativeTeamCreate) -> RDInitiativeTeam:
    """Add a team member to an initiative"""
    db_team_member = RDInitiativeTeam(**team_member.model_dump())
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team_member)
    return db_team_member


def update_team_member(db: Session, team_member_id: int, team_member: RDInitiativeTeamUpdate) -> Optional[RDInitiativeTeam]:
    """Update a team member assignment"""
    db_team_member = get_team_member(db, team_member_id)
    if db_team_member:
        update_data = team_member.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_team_member, field, value)
        db.commit()
        db.refresh(db_team_member)
    return db_team_member


def delete_team_member(db: Session, team_member_id: int) -> bool:
    """Remove a team member from an initiative"""
    db_team_member = get_team_member(db, team_member_id)
    if db_team_member:
        db.delete(db_team_member)
        db.commit()
        return True
    return False