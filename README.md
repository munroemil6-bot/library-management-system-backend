# Smart Library Management System - Backend

## Project Description

The Smart Library Management System is a Flask REST API designed to manage library operations efficiently. It allows users to register, log in, browse books, borrow and return books, while providing librarians with tools to manage books, authors, categories, and users.

This project is being developed as a group project to demonstrate backend development using Flask and RESTful API principles.




---

## Current Progress

### Completed Features

- Flask project setup
- Application Factory Pattern
- SQLAlchemy database configuration
- SQLite database integration
- Flask-Migrate setup
- Marshmallow schemas
- User registration
- User login
- User logout
- Password hashing using Flask-Bcrypt
- User CRUD operations
- Borrow book endpoint
- Return book endpoint
- Database migrations
- Initial database creation
- Docker setup (in progress)

---


---

## Features In Progress

- Book CRUD operations
- Author CRUD operations
- Category CRUD operations
- API testing with Postman
- Docker image optimization
- React frontend integration

---

## Technologies Used

- Python 3.12
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask Marshmallow
- Flask Bcrypt
- Flask Login
- Marshmallow
- SQLite
- Docker
- Gunicorn
- Git
- GitHub

---

## Project Structure

```text
backend/
│
├── library/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── seed.py
│   ├── uploads/
│   ├── static/
│   └── templates/
│
├── migrations/
├── instance/
├── tests/
├── run.py
├── requirements.txt
├── Dockerfile
├── README.md
└── Pipfile
```

---

## Database Models

The application currently includes the following models:

- User
- Author
- Category
- Book
- BorrowRecord

Database management is handled using SQLAlchemy and Flask-Migrate.

---

## Authentication

The authentication system currently supports:

- User Registration
- User Login
- User Logout
- Password Hashing

Passwords are securely hashed before being stored in the database.

---

## Available API Endpoints

### Authentication

| Method | Endpoint |
|---------|----------|
| POST | /register |
| POST | /login |
| POST | /logout |

### Users

| Method | Endpoint |
|---------|----------|
| GET | /users |
| GET | /users/<id> |
| PATCH | /users/<id> |
| DELETE | /users/<id> |

### Borrow Records

| Method | Endpoint |
|---------|----------|
| GET | /borrow |
| POST | /borrow |
| PATCH | /borrow/<id> |
| DELETE | /borrow/<id> |

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd backend
```

Install dependencies

```bash
pipenv install
pipenv shell
```

Run the application

```bash
python run.py
```

or

```bash
flask run
```

---

## Database Migration

Initialize migrations (only once)

```bash
flask db init
```

Create a migration

```bash
flask db migrate -m "Initial database"
```

Apply the migration

```bash
flask db upgrade
```

---

## Seeding the Database

Populate the database with sample data.

```bash
python library/seed.py
```

---

## Docker

Build the Docker image

```bash
docker build -t ciphermun/library-backend:latest .
```

Run the Docker container

```bash
docker run -p 8000:8000 ciphermun/library-backend:latest
```

Push the image to Docker Hub

```bash
docker push ciphermun/library-backend:latest
```

---

## Testing

The backend is tested using:

- Postman
- SQLite Viewer
- Flask Development Server

---

## Planned Improvements

Future enhancements include:

- JWT Authentication
- Role-Based Access Control
- Book Search and Filtering
- Book Reservation System
- Email Notifications
- Fine Management
- Pagination
- PostgreSQL Database Support
- Continuous Integration and Deployment (CI/CD)
- React Frontend Integration
- Automated Unit Testing

---

## Team Members

| Member | Responsibility |
|----------|----------------|
| Myles Munroe | Project Manager, Authentication, Database Design, Backend Integration, Docker |
| Mason | User Authentication and User Management |
| Naomi | Books, Authors and Categories |
| Nasra | Borrowing System and API Testing |

---

## Learning Objectives

This project demonstrates practical knowledge of:

- Flask Application Factory Pattern
- RESTful API Development
- SQLAlchemy ORM
- Database Design
- Database Migrations
- Authentication
- Password Hashing
- Marshmallow Serialization
- Docker Containerization
- Git Collaboration
- Backend Architecture

---

## License

This project was developed for educational purposes as part of a Software Engineering learning program.