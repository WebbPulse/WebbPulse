"""add_education_and_certifications_tables

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-09 00:00:01.000000

"""

from datetime import date
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SEED_EDUCATION = [
    {
        "degree": "Bachelor of Science in Information Networking and Telecommunications",
        "school": "Fort Hays State University",
        "location": "Hays, KS",
        "period": "August 2018 - May 2022",
        "start_date": date(2018, 8, 1),
        "end_date": date(2022, 5, 31),
        "description": (
            "Focused on networking, telecommunications, and information systems. "
            "Served as President of the Advanced Technology Student Organization."
        ),
        "order": 10,
        "is_active": True,
    },
]


SEED_CERTIFICATIONS = [
    {
        "name": "AWS Certified Cloud Practitioner",
        "issuer": "Amazon Web Services",
        "issued_date": date(2023, 1, 1),
        "credential_url": None,
        "order": 10,
        "is_active": True,
    },
    {
        "name": "CCNA: Switching, Routing, and Wireless Essentials",
        "issuer": "Cisco",
        "issued_date": date(2022, 1, 1),
        "credential_url": None,
        "order": 20,
        "is_active": True,
    },
    {
        "name": "CCNA: Enterprise Networking, Security, and Automation",
        "issuer": "Cisco",
        "issued_date": date(2022, 1, 1),
        "credential_url": None,
        "order": 30,
        "is_active": True,
    },
    {
        "name": "Microsoft Certified: Azure Fundamentals",
        "issuer": "Microsoft",
        "issued_date": date(2022, 1, 1),
        "credential_url": None,
        "order": 40,
        "is_active": True,
    },
]


def upgrade() -> None:
    """Upgrade schema."""
    education = op.create_table(
        "education",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("degree", sa.String(), nullable=False),
        sa.Column("school", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("period", sa.String(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
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
    op.create_index(op.f("ix_education_id"), "education", ["id"], unique=False)
    op.create_index(op.f("ix_education_order"), "education", ["order"], unique=False)

    certifications = op.create_table(
        "certifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("issuer", sa.String(), nullable=False),
        sa.Column("issued_date", sa.Date(), nullable=False),
        sa.Column("credential_url", sa.String(), nullable=True),
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
    op.create_index(
        op.f("ix_certifications_id"), "certifications", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_certifications_order"), "certifications", ["order"], unique=False
    )

    op.bulk_insert(education, SEED_EDUCATION)
    op.bulk_insert(certifications, SEED_CERTIFICATIONS)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_certifications_order"), table_name="certifications")
    op.drop_index(op.f("ix_certifications_id"), table_name="certifications")
    op.drop_table("certifications")
    op.drop_index(op.f("ix_education_order"), table_name="education")
    op.drop_index(op.f("ix_education_id"), table_name="education")
    op.drop_table("education")
