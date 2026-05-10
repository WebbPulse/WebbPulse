from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

SkillCategory = Literal["frontend", "backend", "devops", "other"]


class SkillBase(BaseModel):
    name: str
    category: SkillCategory
    proficiency: int = Field(default=50, ge=0, le=100)
    icon: Optional[str] = None
    order: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[SkillCategory] = None
    proficiency: Optional[int] = Field(default=None, ge=0, le=100)
    icon: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class Skill(SkillBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SkillList(BaseModel):
    id: int
    name: str
    category: SkillCategory
    proficiency: int
    icon: Optional[str] = None
    order: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
