from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....core.security import get_current_user
from ....database import get_db
from ....models import SiteContent, User
from ....schemas import SiteContent as SiteContentSchema
from ....schemas import SiteContentUpdate

router = APIRouter()

SINGLETON_ID = 1


@router.get("/", response_model=SiteContentSchema)
async def get_site_content(db: Session = Depends(get_db)):
    """Get the singleton site content row."""
    content = db.query(SiteContent).filter(SiteContent.id == SINGLETON_ID).first()
    if not content:
        raise HTTPException(
            status_code=500, detail="Site content not initialized"
        )
    return content


@router.put("/", response_model=SiteContentSchema)
async def update_site_content(
    update: SiteContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update the singleton site content row (admin only)."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="Not authorized to update site content"
        )

    content = db.query(SiteContent).filter(SiteContent.id == SINGLETON_ID).first()
    if not content:
        raise HTTPException(
            status_code=500, detail="Site content not initialized"
        )

    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(content, field, value)

    db.commit()
    db.refresh(content)
    return content
