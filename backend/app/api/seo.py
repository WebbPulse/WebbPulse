"""SEO endpoints served at the application root.

These are mounted on the app root (not under /api/v1) and exposed at
https://api.webbpulse.com/sitemap.xml and /robots.txt. The sitemap lists
the canonical public site URLs (settings.SITE_URL, i.e. the www host),
not the API host. A blog post counts as public when published_at is set
-- the same rule the public posts endpoints use.
"""

from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Post

router = APIRouter()


def _iso(dt) -> str | None:
    """Render a datetime as a sitemap lastmod (W3C / ISO 8601), or None."""
    return dt.date().isoformat() if dt else None


@router.get("/sitemap.xml", include_in_schema=False)
async def sitemap(db: Session = Depends(get_db)) -> Response:
    base = settings.SITE_URL.rstrip("/")

    # Static public routes (admin is intentionally excluded).
    urls: list[dict] = [
        {"loc": f"{base}/", "changefreq": "monthly", "priority": "1.0"},
        {"loc": f"{base}/blog", "changefreq": "weekly", "priority": "0.8"},
    ]

    posts = (
        db.query(Post)
        .filter(Post.published_at.isnot(None))
        .order_by(Post.published_at.desc())
        .all()
    )
    for post in posts:
        urls.append(
            {
                "loc": f"{base}/blog/{post.slug}",
                "lastmod": _iso(post.updated_at or post.published_at),
                "changefreq": "monthly",
                "priority": "0.6",
            }
        )

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(u['loc'])}</loc>")
        if u.get("lastmod"):
            lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    return Response(
        content="\n".join(lines) + "\n",
        media_type="application/xml",
    )


@router.get("/robots.txt", include_in_schema=False)
async def robots() -> Response:
    base = settings.SITE_URL.rstrip("/")
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        f"Sitemap: {base}/sitemap.xml\n"
    )
    return Response(content=body, media_type="text/plain")
