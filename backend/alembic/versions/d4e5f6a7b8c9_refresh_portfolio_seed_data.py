"""refresh_portfolio_seed_data

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-05-09 21:00:00.000000

Refreshes seeded portfolio content with real data from the LinkedIn profile:
- Fixes site_content.github_url (Tylert2610 -> TW-WebbPulse)
- Points resume_url at /Profile.pdf (committed under frontend/public/)
- Fills in experience.achievements + tightens descriptions
- Adds Dean's Honor Roll to the education entry
- Seeds two placeholder projects (WebbPulse, CarModPicker)

Idempotent enough to re-run on a fresh DB; on existing rows it UPDATEs by
deterministic key (company+title for experience, school for education,
title for projects).
"""

import json
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "c3d4e5f6a7b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


EXPERIENCE_UPDATES = [
    {
        "company": "Verkada",
        "title": "Software Engineer",
        "description": (
            "Software engineer at Verkada, building privacy-conscious physical "
            "security software across cameras, access control, and sensors."
        ),
        "technologies": ["Python", "TypeScript", "React", "FastAPI", "SQL"],
        "achievements": [
            "Promoted from Senior Escalation Engineer into a full-time software role.",
            "Ship features and tooling used by the support and escalation orgs I came from.",
        ],
    },
    {
        "company": "Verkada",
        "title": "Senior Escalation Engineer",
        "description": (
            "Led escalation engineering for the most complex customer issues "
            "spanning device firmware, networking, and cloud services. Mentored "
            "junior engineers and authored runbooks adopted across the team."
        ),
        "technologies": ["Python", "SQL", "Linux", "Datadog", "Networking"],
        "achievements": [
            "Owned cross-team root-cause investigations on the highest-severity escalations.",
            "Built internal automation that cut repetitive escalation triage time materially.",
            "Mentored escalation engineers and wrote playbooks adopted org-wide.",
        ],
    },
    {
        "company": "Verkada",
        "title": "Escalation Engineer",
        "description": (
            "Investigated and resolved escalated technical issues across device "
            "firmware, networking, and Verkada's cloud platform. Partnered with "
            "engineering to drive permanent fixes for recurring problems."
        ),
        "technologies": ["Python", "SQL", "Linux", "Wireshark", "Networking"],
        "achievements": [
            "Drove root-cause analysis on tier-3 issues escalated from global support.",
            "Filed reproducible bug reports that closed long-standing platform defects.",
        ],
    },
    {
        "company": "Verkada",
        "title": "Senior Technical Support Engineer",
        "description": (
            "Senior technical support engineer handling complex enterprise "
            "escalations and mentoring junior teammates on networking, Linux, "
            "and the Verkada platform."
        ),
        "technologies": ["Networking", "Linux", "SQL", "Active Directory"],
        "achievements": [
            "Resolved complex enterprise escalations across networking and access control.",
            "Onboarded and mentored newer technical support engineers.",
        ],
    },
    {
        "company": "Verkada",
        "title": "Technical Support Engineer",
        "description": (
            "Supported enterprise customers deploying Verkada cameras, access "
            "control, and sensors across mixed network environments."
        ),
        "technologies": ["Networking", "Linux", "Wireshark"],
        "achievements": [
            "Diagnosed and resolved customer issues spanning networking, hardware, and cloud config.",
            "Contributed knowledge-base articles still referenced by the support team.",
        ],
    },
    {
        "company": "Midwest Energy, Inc.",
        "title": "Network Engineer",
        "description": (
            "Network engineer at a regional electric and gas utility. Worked on "
            "switching, routing, and wireless infrastructure supporting field "
            "operations across western Kansas."
        ),
        "technologies": ["Cisco", "Networking", "Active Directory"],
        "achievements": [
            "Maintained and upgraded Cisco switching and wireless infrastructure.",
            "Supported field operations across a multi-site utility network.",
        ],
    },
]


EDUCATION_DESCRIPTION = (
    "Focused on networking, telecommunications, and information systems. "
    "Served as President of the Advanced Technology Student Organization. "
    "Dean's Honor Roll."
)


SEED_PROJECTS = [
    {
        "title": "WebbPulse",
        "description": (
            "This site. A full-stack personal portfolio and blog: React + "
            "TypeScript frontend, FastAPI + PostgreSQL backend, deployed on "
            "AWS via Terraform with an admin panel that drives every section "
            "from the API."
        ),
        "image": None,
        "technologies": [
            "React",
            "TypeScript",
            "Tailwind CSS",
            "FastAPI",
            "Python",
            "PostgreSQL",
            "AWS",
            "Terraform",
        ],
        "github_url": "https://github.com/WebbPulse/WebbPulse",
        "live_url": "https://webbpulse.com",
        "featured": True,
        "is_active": True,
    },
    {
        "title": "CarModPicker",
        "description": (
            "A side project for cataloging and planning car modifications. "
            "Python/FastAPI backend with a typed frontend; currently a private "
            "work-in-progress while the schema and scrapers stabilize."
        ),
        "image": None,
        "technologies": ["Python", "FastAPI", "PostgreSQL", "TypeScript"],
        "github_url": None,
        "live_url": None,
        "featured": False,
        "is_active": True,
    },
]


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    # --- site_content fixes ---------------------------------------------------
    bind.execute(
        sa.text(
            """
            UPDATE site_content
            SET github_url = :github_url,
                resume_url = :resume_url,
                updated_at = now()
            WHERE id = 1
            """
        ),
        {
            "github_url": "https://github.com/TW-WebbPulse",
            "resume_url": "/Profile.pdf",
        },
    )

    # --- experience updates ---------------------------------------------------
    for entry in EXPERIENCE_UPDATES:
        bind.execute(
            sa.text(
                """
                UPDATE experience
                SET description = :description,
                    technologies = CAST(:technologies AS JSON),
                    achievements = CAST(:achievements AS JSON),
                    updated_at = now()
                WHERE company = :company AND title = :title
                """
            ),
            {
                "company": entry["company"],
                "title": entry["title"],
                "description": entry["description"],
                "technologies": json.dumps(entry["technologies"]),
                "achievements": json.dumps(entry["achievements"]),
            },
        )

    # --- education update -----------------------------------------------------
    bind.execute(
        sa.text(
            """
            UPDATE education
            SET description = :description,
                updated_at = now()
            WHERE school = :school
            """
        ),
        {
            "description": EDUCATION_DESCRIPTION,
            "school": "Fort Hays State University",
        },
    )

    # --- projects seed (only if title doesn't exist yet) ----------------------
    for project in SEED_PROJECTS:
        existing = bind.execute(
            sa.text("SELECT id FROM projects WHERE title = :title"),
            {"title": project["title"]},
        ).fetchone()
        if existing:
            continue
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
                "title": project["title"],
                "description": project["description"],
                "image": project["image"],
                "technologies": json.dumps(project["technologies"]),
                "github_url": project["github_url"],
                "live_url": project["live_url"],
                "featured": project["featured"],
                "is_active": project["is_active"],
            },
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    # Revert site_content to the previous seed values from c3d4e5f6a7b8
    bind.execute(
        sa.text(
            """
            UPDATE site_content
            SET github_url = :github_url,
                resume_url = NULL,
                updated_at = now()
            WHERE id = 1
            """
        ),
        {"github_url": "https://github.com/Tylert2610"},
    )

    # Drop the seeded projects we added (idempotent)
    for project in SEED_PROJECTS:
        bind.execute(
            sa.text("DELETE FROM projects WHERE title = :title"),
            {"title": project["title"]},
        )

    # Education + experience descriptions/achievements aren't safely reversible
    # to a unique prior state, so we leave them as-is on downgrade.
