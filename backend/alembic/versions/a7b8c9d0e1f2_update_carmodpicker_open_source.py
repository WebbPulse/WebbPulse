"""update_carmodpicker_open_source

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-05-09 22:55:00.000000

CarModPicker is now public at github.com/WebbPulse/CarModPicker and live
at carmodpicker.com. Updates the project row with real description,
links, and a fuller tech stack so a fresh DB matches prod.
"""

import json
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "a7b8c9d0e1f2"
down_revision: Union[str, Sequence[str], None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NEW_DESCRIPTION = (
    "Open-source web app for tracking car modifications: users manage cars "
    "and build lists, attach parts to phased builds, and log progress in "
    "forum-style threads. Companion Chrome extension scrapes part data from "
    "retailer pages. Live at carmodpicker.com."
)
NEW_TECHNOLOGIES = [
    "FastAPI",
    "Python",
    "PostgreSQL",
    "React",
    "TypeScript",
    "Vite",
    "Tailwind CSS",
    "AWS",
    "Terraform",
    "Chrome Extension",
]
NEW_GITHUB_URL = "https://github.com/WebbPulse/CarModPicker"
NEW_LIVE_URL = "https://www.carmodpicker.com"


def upgrade() -> None:
    """Upgrade schema."""
    op.get_bind().execute(
        sa.text(
            """
            UPDATE projects
            SET description = :description,
                technologies = CAST(:technologies AS JSON),
                github_url = :github_url,
                live_url = :live_url,
                updated_at = now()
            WHERE title = :title
            """
        ),
        {
            "description": NEW_DESCRIPTION,
            "technologies": json.dumps(NEW_TECHNOLOGIES),
            "github_url": NEW_GITHUB_URL,
            "live_url": NEW_LIVE_URL,
            "title": "CarModPicker",
        },
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert to the placeholder values from d4e5f6a7b8c9
    prior_description = (
        "A side project for cataloging and planning car modifications. "
        "Python/FastAPI backend with a typed frontend; currently a private "
        "work-in-progress while the schema and scrapers stabilize."
    )
    prior_technologies = ["Python", "FastAPI", "PostgreSQL", "TypeScript"]

    op.get_bind().execute(
        sa.text(
            """
            UPDATE projects
            SET description = :description,
                technologies = CAST(:technologies AS JSON),
                github_url = NULL,
                live_url = NULL,
                updated_at = now()
            WHERE title = :title
            """
        ),
        {
            "description": prior_description,
            "technologies": json.dumps(prior_technologies),
            "title": "CarModPicker",
        },
    )
