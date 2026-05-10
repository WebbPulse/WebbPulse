from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....core.security import get_current_user
from ....database import get_db
from ....models import Skill, User
from ....schemas import Skill as SkillSchema
from ....schemas import SkillCreate, SkillList, SkillUpdate

router = APIRouter()


@router.get("/", response_model=List[SkillList])
async def get_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Get all active skills, ordered by (order, name)"""
    skills = (
        db.query(Skill)
        .filter(Skill.is_active)
        .order_by(Skill.order.asc(), Skill.name.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return skills


@router.get("/{skill_id}", response_model=SkillSchema)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get a single skill by ID"""
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.is_active).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("/", response_model=SkillSchema)
async def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new skill (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create skills")

    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.put("/{skill_id}", response_model=SkillSchema)
async def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a skill (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update skills")

    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    update_data = skill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill, field, value)

    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.delete("/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a skill (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete skills")

    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db_skill.is_active = False
    db.commit()

    return {"message": "Skill deleted successfully"}
