# Hemis Login with FastAPI

A FastAPI-based OAuth2 login system designed for integration with the [Hemis](https://hemis.uz) platform. Built to be minimal, secure, and easily extensible for university or educational portal needs.

---

## 🚀 Features

- 🔐 OAuth2 authentication for Hemis
- 🔑 JWT-based session handling
- 🧪 Easy local development with environment configuration
- 🐘 PostgreSQL database support
- 🐳 Docker-ready

---

## 🛠️ Tech Stack

- Python 3.13+
- FastAPI
- OAuth2 (with Hemis)
- PostgreSQL
- SQLAlchemy
- JWT
- Uvicorn
- python-dotenv

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nomozovasror/hemis_login_with_fastapi.git
cd hemis_login_with_fastapi
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## 📄 Environment Configuration

Create a `.env` file in the root of your project with the following content:

### ✅ `.env` Example

```env
UNIVER=tersu
URL=http://127.0.0.1:8000
API_PORT=8000

# Hemis OAuth2 Credentials
OAUTH2_CLIENT_ID=your-client-id
OAUTH2_CLIENT_SECRET=your-client-secret
OAUTH2_REDIRECT_URI=${URL}/users/auth

# JWT Secret Key
SECRET_KEY=your-secret-key  # Generate with: openssl rand -hex 32

# PostgreSQL Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

> ℹ️ **Tip**: You can generate a secure `SECRET_KEY` with the following command:
> ```bash
> openssl rand -hex 32
> ```

---

## ▶️ Running the App

### Locally with Uvicorn:

```bash
uvicorn main:app --reload
```

Open your browser and navigate to:  
👉 `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## 🐳 Docker (Optional)

### 1. Build the Docker compose

```bash
docker compose up --build
```

---

## 📡 API Endpoints

| Method | Endpoint               | Description                            |
|--------|------------------------|----------------------------------------|
| GET    | `/users/login`         | Redirect to Hemis OAuth2               |
| GET    | `/users/auth`          | OAuth2 redirect URI (callback handler) |
| GET    | `/users/me`            | Get current authenticated user         |

---

## ✅ To-Do

- [ ] Add token refresh flow
- [ ] Role-based permission control
- [ ] Admin interface
- [ ] Unit & integration tests

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue to discuss what you want to change.

---
