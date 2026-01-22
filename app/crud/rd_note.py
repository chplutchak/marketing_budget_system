from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.rd_initiative import RDNote
from app.schemas.rd_note import RDNoteCreate, RDNoteUpdate


def get_note(db: Session, note_id: int) -> Optional[RDNote]:
    """Get a single note"""
    return db.query(RDNote).filter(RDNote.id == note_id).first()


def get_notes_by_initiative(
    db: Session,
    initiative_id: int,
    department: Optional[str] = None
) -> List[RDNote]:
    """Get all notes for an initiative"""
    query = db.query(RDNote).filter(RDNote.initiative_id == initiative_id)
    
    if department:
        query = query.filter(RDNote.department == department)
    
    return query.order_by(RDNote.note_date.desc()).all()


def create_note(db: Session, note: RDNoteCreate) -> RDNote:
    """Create a new note"""
    db_note = RDNote(**note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(
    db: Session,
    note_id: int,
    note: RDNoteUpdate
) -> Optional[RDNote]:
    """Update note"""
    db_note = get_note(db, note_id)
    if not db_note:
        return None
    
    update_data = note.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    """Delete note"""
    db_note = get_note(db, note_id)
    if not db_note:
        return False
    
    db.delete(db_note)
    db.commit()
    return True