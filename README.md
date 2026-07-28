# BookBarn Backend

## Overview

BookBarn Backend is a RESTful API built using Flask. It provides authentication, library management, borrowing functionality, and communicates with the React frontend.

---

# Technologies

- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask Login
- Flask Bcrypt
- Flask Marshmallow
- Flask CORS
- SQLite (Development)
- PostgreSQL (Production)
- Docker
- Gunicorn

---

# Backend Responsibilities

The backend is responsible for:

- User Authentication
- Password Hashing
- User Authorization
- Database Management
- CRUD Operations
- API Endpoints
- Business Logic
- Validation
- Session Management
- Database Relationships

---

# Database Models

## User

- id
- username
- email
- password_hash
- role
- created_at

---

## Author

- id
- name
- biography

---

## Category

- id
- name
- description

---

## Book

- id
- title
- isbn
- description
- published_year
- copies
- available_copies
- author_id
- category_id

---

## BorrowRecord

- id
- borrow_date
- due_date
- return_date
- status
- user_id
- book_id

---

# Project Structure

backend/

```
backend/
│
├── app.py
├── config.py
├── seed.py
├── extensions.py
│
├── models.py
├── routes.py
├── schemas.py
│
├── instance/
├── migrations/
├── uploads/
├── static/
│
├── Dockerfile
├── requirements.txt
├── Pipfile
├── Pipfile.lock
├── .env
└── README.md
```

---

# Development Phases

## Phase 1

- Setup Flask project
- Configure virtual environment
- Install dependencies
- Configure Flask app
- Configure SQLAlchemy
- Configure Flask Login
- Configure Flask Bcrypt
- Configure Marshmallow
- Configure CORS

---

## Phase 2

Create Database Models

- User
- Author
- Category
- Book
- BorrowRecord

Create Relationships

Run

```
flask db init
flask db migrate
flask db upgrade
```

---

## Phase 3

Create Marshmallow Schemas

- UserSchema
- AuthorSchema
- CategorySchema
- BookSchema
- BorrowSchema

Add validations.

---

## Phase 4

Authentication

Implement

- Register
- Login
- Logout

Password hashing

Session management

Role-based authorization

---

## Phase 5

Build REST API

Authentication

```
POST /register
POST /login
POST /logout
```

Users

```
GET
GET /<id>
PATCH
DELETE
```

Books

```
GET
GET /<id>
POST
PATCH
DELETE
```

Authors

```
GET
POST
PATCH
DELETE
```

Categories

```
GET
POST
PATCH
DELETE
```

Borrow Records

```
GET
POST
PATCH
DELETE
```

---

## Phase 6

Testing

- Postman
- API Validation
- Relationship Testing
- Authentication Testing

---

## Phase 7

Deployment

- Docker
- Docker Hub
- Render
- PostgreSQL

---

# Installation

Clone repository

```
git clone <repository-url>
```

Install dependencies

```
pipenv install
```

Activate virtual environment

```
pipenv shell
```

Run migrations

```
flask db upgrade
```

Start server

```
python app.py
```

---

# Expected Outcome

A secure, scalable RESTful API providing authentication, library management, and borrowing services for the BookBarn frontend.
