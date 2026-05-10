from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....core.security import get_current_user
from ....database import get_db
from ....models import Education, User
from ....schemas import Education as EducationSchema
from ....schemas import EducationCreate, EducationList, EducationUpdate

router = APIRouter()


@router.get("/", response_model=List[EducationList])
async def get_education(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all active education entries, ordered by (order asc, start_date desc)."""
    entries = (
        db.query(Education)
        .filter(Education.is_active)
        .order_by(Education.order.asc(), Education.start_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return entries


@router.get("/{education_id}", response_model=EducationSchema)
async def get_education_entry(education_id: int, db: Session = Depends(get_db)):
    """Get a single education entry by ID."""
    entry = (
        db.query(Education)
        .filter(Education.id == education_id, Education.is_active)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Education entry not found")
    return entry


@router.post("/", response_model=EducationSchema)
async def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new education entry (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to create education entries"
        )
    db_entry = Education(**education.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.put("/{education_id}", response_model=EducationSchema)
async def update_education(
    education_id: int,
    education_update: EducationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an education entry (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to update education entries"
        )
    db_entry = db.query(Education).filter(Education.id == education_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Education entry not found")

    update_data = education_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entry, field, value)

    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.delete("/{education_id}")
async def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete an education entry (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete education entries"
        )
    db_entry = db.query(Education).filter(Education.id == education_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Education entry not found")

    db_entry.is_active = False
    db.commit()
    return {"message": "Education entry deleted successfully"}
