import logging

from ..config import settings
from ..core.security import get_password_hash, verify_password
from ..database import SessionLocal
from ..models.user import User

logger = logging.getLogger(__name__)


def seed_admin_user() -> None:
    """Ensure the admin user defined in settings exists and matches env values.

    Idempotent: creates the user on first run, then updates email/password on
    subsequent runs only if they differ from the current values in env.
    """
    db = SessionLocal()
    try:
        user = (
            db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        )

        if user is None:
            user = User(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                is_admin=True,
                is_active=True,
            )
            db.add(user)
            db.commit()
            logger.info(f"Seeded admin user '{settings.ADMIN_USERNAME}'")
            return

        changed = False
        if user.email != settings.ADMIN_EMAIL:
            user.email = settings.ADMIN_EMAIL
            changed = True
        if not verify_password(settings.ADMIN_PASSWORD, user.hashed_password):
            user.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            changed = True
        if not user.is_admin:
            user.is_admin = True
            changed = True
        if not user.is_active:
            user.is_active = True
            changed = True

        if changed:
            db.commit()
            logger.info(f"Updated admin user '{settings.ADMIN_USERNAME}' from env")
    finally:
        db.close()
