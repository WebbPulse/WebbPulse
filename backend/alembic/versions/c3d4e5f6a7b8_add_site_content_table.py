"""add_site_content_table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-09 00:00:02.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SEED_HERO_TITLE = "Hi, I'm Tyler Webb"
SEED_HERO_SUBTITLE = "Software Engineer"
SEED_HERO_DESCRIPTION = (
    "Software engineer at Verkada, building privacy-conscious physical security "
    "software. Background in network engineering and full-stack web."
)
SEED_ABOUT_PARAGRAPHS = [
    (
        "Hi, I'm Tyler. I'm a software engineer at Verkada, where I work on "
        "systems that protect people and property in a privacy-sensitive way. "
        "Before moving into engineering full time, I spent ~4 years as a "
        "technical and escalation engineer there, and started my career as a "
        "network engineer at Midwest Energy."
    ),
    (
        "Outside of work I build personal projects (this site included) — "
        "usually full-stack TypeScript and React on the frontend, Python and "
        "FastAPI on the backend, deployed on AWS via Terraform."
    ),
]
SEED_ABOUT_VALUES = [
    {
        "title": "Clean Code",
        "description": (
            "Writing maintainable, well-documented code that others can easily "
            "understand and build upon."
        ),
        "icon": "✨",
    },
    {
        "title": "User Experience",
        "description": (
            "Creating intuitive, accessible interfaces that provide delightful "
            "user experiences."
        ),
        "icon": "🎨",
    },
    {
        "title": "Continuous Learning",
        "description": (
            "Staying up-to-date with the latest technologies and best practices "
            "in software engineering."
        ),
        "icon": "📚",
    },
]
SEED_FOOTER_TAGLINE = (
    "Software engineer focused on building reliable, privacy-conscious systems."
)


def upgrade() -> None:
    """Upgrade schema."""
    site_content = op.create_table(
        "site_content",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hero_title", sa.Text(), nullable=False),
        sa.Column("hero_subtitle", sa.Text(), nullable=False),
        sa.Column("hero_description", sa.Text(), nullable=False),
        sa.Column("about_paragraphs", sa.JSON(), nullable=False),
        sa.Column("about_values", sa.JSON(), nullable=False),
        sa.Column("profile_image_url", sa.String(), nullable=True),
        sa.Column("resume_url", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("github_url", sa.String(), nullable=True),
        sa.Column("linkedin_url", sa.String(), nullable=True),
        sa.Column("footer_tagline", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("id = 1", name="site_content_singleton"),
    )

    op.bulk_insert(
        site_content,
        [
            {
                "id": 1,
                "hero_title": SEED_HERO_TITLE,
                "hero_subtitle": SEED_HERO_SUBTITLE,
                "hero_description": SEED_HERO_DESCRIPTION,
                "about_paragraphs": SEED_ABOUT_PARAGRAPHS,
                "about_values": SEED_ABOUT_VALUES,
                "profile_image_url": "/headshot.jpg",
                "resume_url": None,
                "email": "tyler@webbpulse.com",
                "github_url": "https://github.com/Tylert2610",
                "linkedin_url": "https://www.linkedin.com/in/tylert2610/",
                "footer_tagline": SEED_FOOTER_TAGLINE,
            }
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("site_content")
