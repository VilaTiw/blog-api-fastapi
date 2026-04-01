# Blog API (FastAPI)

REST API for managing users and articles with authentication and role-based access control (RBAC).

## 🚀 Features

* **Authentication:** JWT (JSON Web Tokens) using `python-jose`.
* **RBAC:** Role-based access control (ADMIN, EDITOR, USER).
* **CRUD:** Full operations for users and articles.
* **Search & Filtering:** Flexible search functionality.
* **Pagination:** Implemented using `limit` and `offset`.
* **Database:** PostgreSQL with SQLAlchemy ORM.
* **Containerization:** Fully dockerized environment (Docker & Docker Compose).
* **Documentation:** Interactive Swagger (OpenAPI) and ReDoc.
* **Data Seeding:** Initial data seeding via SQL scripts.

---

## 🧱 Tech Stack

* **Python** 3.11+
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Docker & Docker Compose**
* **JWT** (`python-jose`)
* **Passlib** (`bcrypt`)

---

## 📦 Project Structure

```text
📦 Project Structure

app/
├── core/          # Configuration, security (JWT, hashing, dependencies)
├── models/        # SQLAlchemy ORM models (User, Article)
├── routers/       # API routes (articles, users, auth)
├── schemas/       # Pydantic schemas (request/response validation)
├── scripts/       # SQL scripts for DB initialization and seeding
├── tests/         # Unit tests
└── main.py        # FastAPI application entry point

docker-compose.yml                # Docker services configuration
Dockerfile                        # Application container definition
requirements.txt                  # Python dependencies
.env.example                      # Example environment variables
Blog API.postman_collection.json  # Postman collection for API testing
README.md                         # Project documentation
```

---

## ⚙️ Environment Variables

The application uses environment variables for configuration. Create a `.env` file in the root directory based on the example below:

```env
DATABASE_URL=postgresql://blog_user:blog_password@db:5432/blog_db
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🐳 Run with Docker

### 1. Build and start containers

```bash
docker compose up --build
```

### 2. Access the application

* **API:** `http://localhost:8000`
* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

### 3. Create a new user (via script)

You can create a user inside the running container using the built-in script:

```bash
docker exec -it blog_app python -m app.scripts.create_user \
  --username some_user \
  --email some@email.com \
  --password some_password \
  --role user
```
### Default Credentials (if seeded)

- email: admin@test.com  
- password: admin123
---

## 🗄️ Database Initialization

The database is automatically initialized using SQL scripts located in `app/scripts/`:
* `init.sql` – creates tables
* `seed.sql` – inserts initial data

These scripts are executed on the first container startup.

---

## 🔐 Authentication

To access protected endpoints:
1. Send a POST request to `/auth/login` to obtain a JWT token.
2. Use the token in the `Authorization` header: `Bearer <your_token>`.
3. In Swagger UI, click **Authorize** and paste your token.

---

## 🧪 Running Tests

Run tests inside the Docker container:

```bash
# Run articles test
docker exec -it blog_app python -m unittest app.tests.test_articles 
# Run users test
docker exec -it blog_app python -m unittest app.tests.test_users 
# Run with coverage report
docker exec -it blog_app coverage report
```
### 📊 Test Coverage
- **Overall coverage:** 89%
- Coverage includes unit tests for core logic, routers, and authentication.

---

## API Endpoints

| Method | Path | Description | Access |
| :--- | :--- | :--- | :--- |
| **GET** | `/health` | Service health check | All |
| **POST** | `/auth/login` | Login and get JWT token | All |

### 👤 Users
| Method | Path | Description | Access |
| :--- | :--- | :--- | :--- |
| **GET** | `/users/` | Get list of users | Admin |
| **GET** | `/users/{user_id}` | Get user by ID | Admin |
| **GET** | `/users/search` | Search users by username or email | Admin |
| **PUT** | `/users/{user_id}` | Update user email and role | Admin |
| **DELETE** | `/users/{user_id}` | Delete a user | Admin |

### 📝 Articles
| Method | Path | Description | Access |
| :--- | :--- | :--- | :--- |
| **GET** | `/articles/` | Get list of articles (paginated) | User/Admin/Editor |
| **GET** | `/articles/{article_id}` | Get article by ID | User/Admin/Editor |
| **GET** | `/articles/search` | Search articles with filters and pagination | User/Admin/Editor |
| **POST** | `/articles/` | Create a new article | User/Admin/Editor |
| **PUT** | `/articles/{article_id}` | Update an article | Owner/Admin/Editor |
| **DELETE** | `/articles/{article_id}` | Delete an article | Owner/Admin |

---


## 👤 Roles

* **ADMIN:** Full access to all resources, including user management.
* **EDITOR:** Can create articles, edit any articles and delete their own articles. No access to user management.
* **USER:** Can create their own articles, edit/delete only their own content, and view others' articles.
---

## ▶️ Stop the application

```bash
docker compose down
```