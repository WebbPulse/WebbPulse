"""add_project_ordering

Revision ID: b9c0d1e2f3a4
Revises: a7b8c9d0e1f2
Create Date: 2026-05-16 00:00:00.000000

Adds manual per-project ordering (projects.display_order) and a site-wide
ordering mode (site_content.project_sort_mode). Featured projects are still
pinned above non-featured ones regardless of mode; the mode controls the
secondary ordering within each group.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "b9c0d1e2f3a4"
down_revision: Union[str, Sequence[str], None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "projects",
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "site_content",
        sa.Column(
            "project_sort_mode",
            sa.String(),
            nullable=False,
            server_default="manual",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("site_content", "project_sort_mode")
    op.drop_column("projects", "display_order")
