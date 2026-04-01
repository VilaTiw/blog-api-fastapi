import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.core.roles import Role
from app.models.user import User
from app.core.dependencies import get_current_user, get_db

from app.tests.config import mock_get_current_user, FakeDB

client = TestClient(app)

class TestArticles(unittest.TestCase):

    def setUp(self):
        self.fake_db_instance = FakeDB()
        app.dependency_overrides[get_current_user] = mock_get_current_user
        app.dependency_overrides[get_db] = lambda: self.fake_db_instance

    def tearDown(self):
        app.dependency_overrides = {}

    def test_get_articles(self):
        response = client.get("/articles/")
        self.assertEqual(response.status_code, 200)

    def test_create_article(self):
        response = client.post("/articles/", json={"title": "test title", "content": "test content"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "test title")

    def test_get_article_not_found(self):
        response = client.get("/articles/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_article(self):
        article = client.post("/articles/", json={"title": "test title", "content": "test content"})
        article_id = article.json()["id"]
        response = client.delete(f"/articles/{article_id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_article(self):
        article = client.post("/articles/", json={"title": "test title", "content": "test content"})
        article_id = article.json()["id"]
        response = client.put(f"/articles/{article_id}/", json={"title": "new title", "content": "new content"})
        self.assertEqual(response.status_code, 200)
        updated_article = response.json()
        self.assertEqual(updated_article["title"], "new title")
        self.assertEqual(updated_article["content"], "new content")

    def test_search_article(self):
        response = client.get("/articles/search?query=invalid")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_delete_article_not_owner(self):
        app.dependency_overrides[get_current_user] = lambda: User(id=2, email="x2@test.com", role=Role.USER.value)
        article = client.post("/articles/", json={"title": "t", "content": "c"})
        article_id = article.json()["id"]

        app.dependency_overrides[get_current_user] = lambda: User(id=3, email="x3@test.com", role=Role.USER.value)
        response = client.delete(f"/articles/{article_id}")
        self.assertEqual(response.status_code, 403)