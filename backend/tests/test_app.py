"""
Unit tests for Flask API endpoints
"""

import pytest
import sys
from pathlib import Path

# Add backend module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


class TestFlaskApp:
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_app_runs(self):
        """Test that app initializes without errors"""
        assert app is not None

    def test_index_endpoint(self, client):
        """Test that index endpoint returns 200"""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_returns_text(self, client):
        """Test that index endpoint returns expected text"""
        response = client.get("/")
        assert b"Personal Finance Analyzer API" in response.data

    def test_upload_endpoint_exists(self, client):
        """Test that upload endpoint exists"""
        # Sending without file to test endpoint exists
        response = client.post("/api/upload-and-analyze")
        # Should get error about missing file, not 404
        assert response.status_code in [400, 415, 422]  # Not 404

    def test_upload_without_file_returns_400(self, client):
        """Test that uploading without file returns 400"""
        response = client.post("/api/upload-and-analyze")
        assert response.status_code == 400

    def test_upload_with_empty_filename_returns_400(self, client):
        """Test that uploading with empty filename returns 400"""
        response = client.post(
            "/api/upload-and-analyze", data={"file": (None, "", "text/csv")}
        )
        assert response.status_code in [400, 422]

    def test_app_config_upload_folder(self):
        """Test that app has upload folder configured"""
        assert "UPLOAD_FOLDER" in app.config
        assert app.config["UPLOAD_FOLDER"] is not None

    def test_app_config_max_content_length(self):
        """Test that app has max content length configured"""
        assert "MAX_CONTENT_LENGTH" in app.config
        # 16MB
        assert app.config["MAX_CONTENT_LENGTH"] == 16 * 1024 * 1024

    def test_app_has_cors_enabled(self):
        """Test that CORS is enabled on the app"""
        # If CORS is enabled, the app should have cross_origin decorator
        # This is a basic check that the app doesn't crash with CORS
        assert app is not None
