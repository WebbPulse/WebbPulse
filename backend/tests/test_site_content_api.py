"""
Tests for the site content singleton API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class TestSiteContentAPI:
    @pytest.mark.api
    def test_get_site_content(self, client: TestClient, test_site_content):
        response = client.get("/api/v1/site-content/")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["hero_title"] == "Hi, I'm Test"
        assert isinstance(data["about_paragraphs"], list)
        assert len(data["about_paragraphs"]) == 2
        assert isinstance(data["about_values"], list)
        assert data["about_values"][0]["title"] == "Test Value"

    @pytest.mark.api
    def test_get_site_content_uninitialized(self, client: TestClient):
        """If the singleton row is missing, return 500."""
        response = client.get("/api/v1/site-content/")
        assert response.status_code == 500


class TestSiteContentAdminAPI:
    @pytest.mark.api
    @pytest.mark.auth
    def test_update_site_content_admin(
        self, client: TestClient, admin_auth_headers, test_site_content
    ):
        response = client.put(
            "/api/v1/site-content/",
            json={"hero_title": "Updated Title"},
            headers=admin_auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["hero_title"] == "Updated Title"
        # Untouched fields preserved
        assert data["hero_subtitle"] == "Test Subtitle"

    @pytest.mark.api
    @pytest.mark.auth
    def test_update_site_content_replaces_arrays(
        self, client: TestClient, admin_auth_headers, test_site_content
    ):
        new_paragraphs = ["Only one paragraph now."]
        new_values = [
            {"title": "New", "description": "Replaced wholesale", "icon": "🔥"},
        ]
        response = client.put(
            "/api/v1/site-content/",
            json={
                "about_paragraphs": new_paragraphs,
                "about_values": new_values,
            },
            headers=admin_auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["about_paragraphs"] == new_paragraphs
        assert len(data["about_values"]) == 1
        assert data["about_values"][0]["title"] == "New"

    @pytest.mark.api
    @pytest.mark.auth
    def test_update_site_content_unauthorized(
        self, client: TestClient, auth_headers, test_site_content
    ):
        response = client.put(
            "/api/v1/site-content/",
            json={"hero_title": "X"},
            headers=auth_headers,
        )
        assert response.status_code == 403

    @pytest.mark.api
    @pytest.mark.auth
    def test_update_site_content_no_auth(
        self, client: TestClient, test_site_content
    ):
        response = client.put("/api/v1/site-content/", json={"hero_title": "X"})
        assert response.status_code == 403

    @pytest.mark.api
    @pytest.mark.auth
    def test_update_site_content_uninitialized(
        self, client: TestClient, admin_auth_headers
    ):
        """PUT without a seeded row should fail (the migration would seed it)."""
        response = client.put(
            "/api/v1/site-content/",
            json={"hero_title": "X"},
            headers=admin_auth_headers,
        )
        assert response.status_code == 500


class TestSiteContentSingletonConstraint:
    @pytest.mark.unit
    def test_cannot_insert_second_row(
        self, db_session: Session, test_site_content
    ):
        """The CHECK(id = 1) constraint must prevent inserting another row."""
        from app.models import SiteContent

        second = SiteContent(
            id=2,
            hero_title="Bad",
            hero_subtitle="Bad",
            hero_description="Bad",
            about_paragraphs=[],
            about_values=[],
        )
        db_session.add(second)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()
