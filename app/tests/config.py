from app.models.user import User
from app.core.roles import Role

def mock_get_current_user():
    return User(id=1, email="test@test.com", role=Role.ADMIN)

class FakeQuery:
    def __init__(self, data):
        self.data = data

    def filter(self, *args, **kwargs):
        return self

    def join(self, *args, **kwargs):
        return self

    def offset(self, offset):
        return self

    def limit(self, limit):
        return self

    def all(self):
        return self.data

    def first(self):
        return self.data[0] if self.data else None


class FakeDB:
    def __init__(self):
        self.articles = []
        self.users = []
        self.counter = 1
        self.user_counter = 1

    def query(self, model):
        if model.__name__ == "User":
            return FakeQuery(self.users)
        return FakeQuery(self.articles)

    def add(self, obj):
        if isinstance(obj, User):
            obj.id = self.user_counter
            self.user_counter += 1
            self.users.append(obj)
        else:
            obj.id = self.counter
            obj.author_id = 1
            self.counter += 1
            self.articles.append(obj)

    def commit(self):
        pass

    def refresh(self, obj):
        pass

    def delete(self, obj):
        if isinstance(obj, User):
            self.users.remove(obj)
        else:
            self.articles.remove(obj)