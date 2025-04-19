# Stack Overflow Clone - Setup and Usage Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Database Setup](#database-setup)
5. [Running the Project](#running-the-project)
6. [Using the Project](#using-the-project)
7. [API Documentation](#api-documentation)
8. [Troubleshooting](#troubleshooting)

## Project Overview

This is a Stack Overflow clone built with:
- Django 5.0.3 (Backend Admin)
- FastAPI 0.109.2 (API)
- MySQL (Database)
- Python 3.13

Features:
- Question & Answer system
- Voting mechanism
- User reputation system
- Tagging system
- Comments
- REST API

## System Requirements

1. Python 3.13 or higher
2. MySQL Server
3. Git
4. macOS, Linux, or Windows

## Installation Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd stackoverflow_clone
```

### 2. Set Up Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

## Database Setup

### 1. Create .env File
Create a file named `.env` in the project root:
```env
DB_NAME=stackoverflow_clone
DB_USER=root
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=3306
```

### 2. Create MySQL Database
```sql
CREATE DATABASE stackoverflow_clone;
```

### 3. Apply Migrations
```bash
# Create database tables
python3 manage.py migrate

# Create admin user
python3 manage.py createsuperuser
```

## Running the Project

The project requires running two servers simultaneously:

### 1. Django Admin Server
Open a terminal and run:
```bash
# Activate virtual environment
source venv/bin/activate

# Start Django server
python3 manage.py runserver 8000
```
You should see:
```
Watching for file changes with StatReloader
Starting development server at http://127.0.0.1:8000/
```

### 2. FastAPI Server
Open another terminal and run:
```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn api.main:app --reload --port 8001
```
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

## Using the Project

### Admin Interface (Django)
1. Access: http://127.0.0.1:8000/admin
2. Login with superuser credentials
3. Available sections:
   - Questions
   - Answers
   - Tags
   - Users
   - Comments
   - Votes

### API Endpoints (FastAPI)
Base URL: http://127.0.0.1:8001

Available endpoints:
1. Root endpoint:
   ```
   GET /
   Response: Welcome message
   ```

2. List Questions:
   ```
   GET /api/questions/
   Response: List of all questions
   ```

3. Get Question:
   ```
   GET /api/questions/{question_id}
   Response: Specific question details
   ```

### Interactive API Documentation
- Swagger UI: http://127.0.0.1:8001/docs
- ReDoc: http://127.0.0.1:8001/redoc

## Project Structure
```
stackoverflow_clone/
├── api/                    # FastAPI application
│   └── main.py            # API endpoints
├── qna/                   # Django app
│   ├── models.py         # Database models
│   ├── admin.py         # Admin interface
│   └── views.py         # Views
├── stackoverflow_clone/   # Project settings
└── manage.py            # Django CLI
```

## Models

### Question Model
- Title (max length: 255)
- Content (text)
- Author (User foreign key)
- Tags (many-to-many)
- Created/Updated timestamps
- View count
- Solved status

### Answer Model
- Content (text)
- Question reference
- Author
- Accepted status
- Created/Updated timestamps

### UserProfile Model
- User reference
- Reputation points
- Bio
- Location
- Avatar

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   ```
   Solution: Check .env file and MySQL credentials
   ```

2. **Port Already in Use**
   ```
   Solution: Change port number in command
   python manage.py runserver 8002  # for Django
   uvicorn api.main:app --port 8003  # for FastAPI
   ```

3. **Module Not Found**
   ```
   Solution: Ensure virtual environment is activated
   source venv/bin/activate
   ```

4. **Migration Issues**
   ```
   Solution: Reset migrations
   python manage.py migrate --fake qna zero
   python manage.py migrate qna
   ```

### Getting Help
- Check the error message in the terminal
- Ensure all services (MySQL, Django, FastAPI) are running
- Verify environment variables in .env file
- Check port availability

## Development Workflow

1. Start MySQL server
2. Run Django server (port 8000)
3. Run FastAPI server (port 8001)
4. Access admin panel
5. Use API endpoints

## Quick Start Commands
```bash
# One-time setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser

# Running servers
# Terminal 1
source venv/bin/activate
python3 manage.py runserver 8000

# Terminal 2
source venv/bin/activate
uvicorn api.main:app --reload --port 8001
```