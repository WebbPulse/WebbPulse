from sqlalchemy import JSON, CheckConstraint, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from ..database import Base


class SiteContent(Base):
    """Singleton table holding site-wide editable content.

    Constrained to a single row (id = 1) at the schema level.
    """

    __tablename__ = "site_content"
    __table_args__ = (CheckConstraint("id = 1", name="site_content_singleton"),)

    id = Column(Integer, primary_key=True, default=1)

    hero_title = Column(Text, nullable=False)
    hero_subtitle = Column(Text, nullable=False)
    hero_description = Column(Text, nullable=False)

    about_paragraphs = Column(JSON, nullable=False, default=list)
    about_values = Column(JSON, nullable=False, default=list)

    profile_image_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)

    email = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)

    footer_tagline = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
