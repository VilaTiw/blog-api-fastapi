import unittest
from fastapi.testclient import TestClient

from app.main import app
from app.core.roles import Role
from app.models.user import User
from app.core.dependencies import get_current_user, get_db

from app.tests.config import mock_get_current_user, FakeDB

client = TestClient(app)

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.fake_db_instance = FakeDB()
        app.dependency_overrides[get_current_user] = mock_get_current_user
        app.dependency_overrides[get_db] = lambda: self.fake_db_instance

        user1 = User(id=2, email="a@test.com", username="alice", role=Role.USER.value)
        user2 = User(id=3, email="b@test.com", username="bob", role=Role.ADMIN.value)

        self.fake_db_instance.users.extend([user1, user2])

    def tearDown(self):
        app.dependency_overrides = {}

    def test_get_users(self):
        response = client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 2)

    def test_get_users_not_allowed(self):
        try:
            app.dependency_overrides[get_current_user] = lambda: User(id=10, email="test@test.com", role=Role.USER.value)
            response = client.get("/users/")
            self.assertEqual(response.status_code, 403)
        finally:
            app.dependency_overrides[get_current_user] = mock_get_current_user

    def test_get_user(self):
        response = client.get("/users/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 2)

    def test_user_not_found(self):
        self.fake_db_instance.users = []
        response = client.get("/users/999")
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        response = client.delete("/users/1")
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        response = client.put("/users/1", json={"email": "new@test.com", "role": Role.ADMIN.value})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "new@test.com")
        self.assertEqual(response.json()["role"], Role.ADMIN)

    def test_search_users(self):
        response = client.get("/users/search?query=ali")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertTrue(any("alice" in u["username"] for u in results))