"""replace_skill_proficiency_with_tier

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-05-09 22:40:00.000000

Replaces skills.proficiency (Integer 0-100) with skills.tier (String enum:
core | working | familiar). Backfills tier from proficiency thresholds:

    proficiency >= 85 -> core
    70 <= p < 85      -> working
    p < 70            -> familiar

Then applies manual overrides to align with self-presentation:
    TypeScript, FastAPI -> core (LinkedIn Top Skills)
    Azure, GCP          -> familiar (not used day-to-day)

Finally drops the proficiency column.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, Sequence[str], None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CORE_OVERRIDES = ["TypeScript", "FastAPI"]
FAMILIAR_OVERRIDES = ["Azure", "GCP"]


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "skills",
        sa.Column(
            "tier",
            sa.String(),
            nullable=False,
            server_default="working",
        ),
    )

    bind = op.get_bind()

    # Backfill from proficiency
    bind.execute(
        sa.text(
            """
            UPDATE skills
            SET tier = CASE
                WHEN proficiency >= 85 THEN 'core'
                WHEN proficiency >= 70 THEN 'working'
                ELSE 'familiar'
            END
            """
        )
    )

    # Manual overrides
    bind.execute(
        sa.text("UPDATE skills SET tier = 'core' WHERE name = ANY(:names)"),
        {"names": CORE_OVERRIDES},
    )
    bind.execute(
        sa.text("UPDATE skills SET tier = 'familiar' WHERE name = ANY(:names)"),
        {"names": FAMILIAR_OVERRIDES},
    )

    # Drop the server_default now that data is populated
    op.alter_column("skills", "tier", server_default=None)

    op.drop_column("skills", "proficiency")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "skills",
        sa.Column(
            "proficiency",
            sa.Integer(),
            nullable=False,
            server_default="50",
        ),
    )

    bind = op.get_bind()
    # Best-effort restore: tier -> a representative number
    bind.execute(
        sa.text(
            """
            UPDATE skills
            SET proficiency = CASE tier
                WHEN 'core' THEN 90
                WHEN 'working' THEN 75
                ELSE 60
            END
            """
        )
    )

    op.alter_column("skills", "proficiency", server_default=None)
    op.drop_column("skills", "tier")
