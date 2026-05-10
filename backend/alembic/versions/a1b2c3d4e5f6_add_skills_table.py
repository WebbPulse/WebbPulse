"""add_skills_table

Revision ID: a1b2c3d4e5f6
Revises: ec5fa6485586
Create Date: 2026-05-09 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "ec5fa6485586"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SEED_SKILLS = [
    # Frontend
    {"name": "React", "category": "frontend", "proficiency": 85, "icon": "⚛️", "order": 10},
    {"name": "TypeScript", "category": "frontend", "proficiency": 80, "icon": "📘", "order": 20},
    {"name": "JavaScript", "category": "frontend", "proficiency": 85, "icon": "🟨", "order": 30},
    {"name": "HTML/CSS", "category": "frontend", "proficiency": 80, "icon": "🎨", "order": 40},
    {"name": "Tailwind CSS", "category": "frontend", "proficiency": 75, "icon": "🎯", "order": 50},
    {"name": "Flutter/Dart", "category": "frontend", "proficiency": 70, "icon": "📱", "order": 60},
    # Backend
    {"name": "Python", "category": "backend", "proficiency": 90, "icon": "🐍", "order": 10},
    {"name": "FastAPI", "category": "backend", "proficiency": 80, "icon": "⚡", "order": 20},
    {"name": "PostgreSQL", "category": "backend", "proficiency": 75, "icon": "🐘", "order": 30},
    {"name": "SQL", "category": "backend", "proficiency": 85, "icon": "🗄️", "order": 40},
    {"name": "Firebase", "category": "backend", "proficiency": 70, "icon": "🔥", "order": 50},
    # DevOps
    {"name": "AWS", "category": "devops", "proficiency": 80, "icon": "☁️", "order": 10},
    {"name": "Docker", "category": "devops", "proficiency": 75, "icon": "🐳", "order": 20},
    {"name": "Kubernetes", "category": "devops", "proficiency": 65, "icon": "⚓", "order": 30},
    {"name": "Git", "category": "devops", "proficiency": 90, "icon": "📚", "order": 40},
    {"name": "Bash", "category": "devops", "proficiency": 85, "icon": "💻", "order": 50},
    {"name": "Datadog", "category": "devops", "proficiency": 80, "icon": "📊", "order": 60},
    # Other
    {"name": "Network Troubleshooting", "category": "other", "proficiency": 85, "icon": "🌐", "order": 10},
    {"name": "Wireshark", "category": "other", "proficiency": 75, "icon": "🔍", "order": 20},
    {"name": "Active Directory", "category": "other", "proficiency": 80, "icon": "🏢", "order": 30},
    {"name": "Azure", "category": "other", "proficiency": 75, "icon": "🔵", "order": 40},
    {"name": "GCP", "category": "other", "proficiency": 70, "icon": "☁️", "order": 50},
    {"name": "Problem Solving", "category": "other", "proficiency": 95, "icon": "🧩", "order": 60},
    {"name": "Technical Documentation", "category": "other", "proficiency": 85, "icon": "📝", "order": 70},
    {"name": "Automation", "category": "other", "proficiency": 90, "icon": "🤖", "order": 80},
]


def upgrade() -> None:
    """Upgrade schema."""
    skills = op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("proficiency", sa.Integer(), nullable=False),
        sa.Column("icon", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_skills_id"), "skills", ["id"], unique=False)
    op.create_index(op.f("ix_skills_order"), "skills", ["order"], unique=False)

    op.bulk_insert(
        skills,
        [{**s, "is_active": True} for s in SEED_SKILLS],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_skills_order"), table_name="skills")
    op.drop_index(op.f("ix_skills_id"), table_name="skills")
    op.drop_table("skills")
