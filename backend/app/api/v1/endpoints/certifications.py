from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....core.security import get_current_user
from ....database import get_db
from ....models import Certification, User
from ....schemas import Certification as CertificationSchema
from ....schemas import CertificationCreate, CertificationList, CertificationUpdate

router = APIRouter()


@router.get("/", response_model=List[CertificationList])
async def get_certifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get all active certifications, ordered by (order asc, issued_date desc)."""
    entries = (
        db.query(Certification)
        .filter(Certification.is_active)
        .order_by(Certification.order.asc(), Certification.issued_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return entries


@router.get("/{certification_id}", response_model=CertificationSchema)
async def get_certification(certification_id: int, db: Session = Depends(get_db)):
    """Get a single certification by ID."""
    entry = (
        db.query(Certification)
        .filter(Certification.id == certification_id, Certification.is_active)
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Certification not found")
    return entry


@router.post("/", response_model=CertificationSchema)
async def create_certification(
    certification: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new certification (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to create certifications"
        )
    db_entry = Certification(**certification.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.put("/{certification_id}", response_model=CertificationSchema)
async def update_certification(
    certification_id: int,
    certification_update: CertificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a certification (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to update certifications"
        )
    db_entry = (
        db.query(Certification).filter(Certification.id == certification_id).first()
    )
    if not db_entry:
        raise HTTPException(status_code=404, detail="Certification not found")

    update_data = certification_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entry, field, value)

    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.delete("/{certification_id}")
async def delete_certification(
    certification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a certification (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete certifications"
        )
    db_entry = (
        db.query(Certification).filter(Certification.id == certification_id).first()
    )
    if not db_entry:
        raise HTTPException(status_code=404, detail="Certification not found")

    db_entry.is_active = False
    db.commit()
    return {"message": "Certification deleted successfully"}
