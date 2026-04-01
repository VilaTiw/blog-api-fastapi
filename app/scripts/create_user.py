import argparse
from ..core.database import SessionLocal
from app.models.user import User
from app.core.roles import Role
from app.core.security import hash_password

def create_user(username, email, role, password):
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.email == email).first()

        if db_user:
            print("User already exists")
            return

        new_user = User(
            username=username,
            email=email,
            role=Role(role.upper()),
            hashed_password=hash_password(password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"User {username} created with email {email} and role {role}.")
    finally:
        db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--role", required=True, choices=["user", "admin", "editor"])
    parser.add_argument("--password", required=True)

    args = parser.parse_args()
    create_user(args.username, args.email, args.role, args.password)