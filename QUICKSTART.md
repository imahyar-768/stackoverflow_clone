 # Quick Start Guide

## 1. First-Time Setup

```bash
# Clone repository and enter directory
git clone <repository-url>
cd stackoverflow_clone

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python3 manage.py migrate

# Create admin user
python3 manage.py createsuperuser
```

## 2. Running the Project

### Terminal 1 (Django Admin):
```bash
source venv/bin/activate
python3 manage.py runserver 8000
```
Access at: http://127.0.0.1:8000/admin

### Terminal 2 (FastAPI):
```bash
source venv/bin/activate
uvicorn api.main:app --reload --port 8001
```
Access at: http://127.0.0.1:8001/docs

## 3. Important URLs

- Django Admin: http://127.0.0.1:8000/admin
- API Documentation: http://127.0.0.1:8001/docs
- API Alternative Docs: http://127.0.0.1:8001/redoc

## 4. Environment Variables (.env)

Create a `.env` file in the project root:
```env
DB_NAME=stackoverflow_clone
DB_USER=root
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=3306
```

## 5. Testing the Setup

1. Visit http://127.0.0.1:8000/admin
2. Log in with superuser credentials
3. Create a test question
4. Visit http://127.0.0.1:8001/api/questions/ to see it in the API