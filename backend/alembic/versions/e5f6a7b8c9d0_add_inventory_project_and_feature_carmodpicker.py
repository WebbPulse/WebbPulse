"""add_inventory_project_and_feature_carmodpicker

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-05-09 22:10:00.000000

Seeds the newly open-sourced WebbPulse Inventory Management project and
flips CarModPicker's featured flag to true. Idempotent on title.
"""

import json
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, Sequence[str], None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


INVENTORY_PROJECT = {
    "title": "WebbPulse Inventory Management",
    "description": (
        "Open-source inventory tracker for organizations checking devices in "
        "and out, originally built to run at inventory.webbpulse.com. "
        "Cross-platform Flutter client (web, iOS, Android, desktop) with a "
        "Firebase backend: Firestore for real-time sync, Auth + custom claims "
        "for per-org roles, and Python Cloud Functions for all mutations and "
        "scheduled Verkada Command sync."
    ),
    "image": None,
    "technologies": [
        "Flutter",
        "Dart",
        "Firebase",
        "Firestore",
        "Cloud Functions",
        "Python",
    ],
    "github_url": "https://github.com/TW-WebbPulse/WebbPulse-Inventory-Management",
    "live_url": None,
    "featured": True,
    "is_active": True,
}


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    # Feature CarModPicker
    bind.execute(
        sa.text(
            """
            UPDATE projects
            SET featured = true,
                updated_at = now()
            WHERE title = :title
            """
        ),
        {"title": "CarModPicker"},
    )

    # Insert inventory project if not already present
    existing = bind.execute(
        sa.text("SELECT id FROM projects WHERE title = :title"),
        {"title": INVENTORY_PROJECT["title"]},
    ).fetchone()
    if existing:
        return

    bind.execute(
        sa.text(
            """
            INSERT INTO projects (
                title, description, image, technologies,
                github_url, live_url, featured, is_active, created_at
            )
            VALUES (
                :title, :description, :image, CAST(:technologies AS JSON),
                :github_url, :live_url, :featured, :is_active, now()
            )
            """
        ),
        {
            "title": INVENTORY_PROJECT["title"],
            "description": INVENTORY_PROJECT["description"],
            "image": INVENTORY_PROJECT["image"],
            "technologies": json.dumps(INVENTORY_PROJECT["technologies"]),
            "github_url": INVENTORY_PROJECT["github_url"],
            "live_url": INVENTORY_PROJECT["live_url"],
            "featured": INVENTORY_PROJECT["featured"],
            "is_active": INVENTORY_PROJECT["is_active"],
        },
    )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM projects WHERE title = :title"),
        {"title": INVENTORY_PROJECT["title"]},
    )
    bind.execute(
        sa.text(
            "UPDATE projects SET featured = false, updated_at = now() "
            "WHERE title = :title"
        ),
        {"title": "CarModPicker"},
    )
