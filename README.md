# Productivity Task Management API

## Project Description

The Productivity Task Management API is a secure RESTful backend built with Flask that allows users to:
   -Secure JWT authentication for users.
   -A user-owned resource (e.g., tasks, notes, or journal entries).
   -Full CRUD functionality with ownership checks.
   -Pagination for resource listing.
   -A seed script to populate the database with sample users and tasks.

Each authenticated user has ownership over their own tasks and cannot access, update, or delete tasks that belong to another user. The application demonstrates secure authentication, authorization, CRUD operations, pagination, password hashing, database migrations, and clean project organization.
___

# Features

## Authentication

- User Registration
- User Login
- JWT Authentication
- Password Hashing using Flask-Bcrypt
- Protected Routes
- Current Authenticated User Endpoint
- Logout Endpoint

___

## Task Management

Authenticated users can:

- Create Tasks
- View Their Tasks
- View Individual Tasks
- Update Tasks
- Delete Tasks
- Mark Tasks as Completed
- Assign Due Dates

___

## Security

- Passwords stored as hashed values
- JWT required for protected endpoints
- Users can only access their own tasks
- Unauthorized requests return appropriate HTTP status codes

___

## Pagination

The task index endpoint supports pagination.

Example:

```
GET /tasks?page=1&per_page=10
```

___


## Tech Stack

 -Flask – Web framework
 -Flask-SQLAlchemy – ORM for database models
 -Flask-Migrate – Database migrations
 -Flask-Bcrypt – Password hashing
 -Flask-JWT-Extended – JWT authentication
 -Marshmallow – Serialization and validation
 -Faker – Database seeding

___

## Project Structure
Flask-Back-end--Productivity/
├── app.py                
├── config.py             
├── requirements.txt      
├── Pipfile               
├── Pipfile.lock
├── README.md             
├── seed.py               
├── .env.example          
├── .gitignore
├── instance/
│   └── app.db            
├── migrations/           
├── server/
│   ├── __init__.py       
│   ├── controllers/      
│   │   ├── auth_controller.py
│   │   └── task_controller.py
│   ├── models/           
│   │   ├── base_model.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/          
│   │   ├── user_schema.py
│   │   └── task_schema.py
│   └── utils/            
│       ├── extensions.py 
│       ├── pagination.py
│       ├── responses.py
│       └── validators.py
└── routes.py             
└── run.py                

___

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Flask-Back-end--Productivity-App.git
```

Navigate into the project

```bash
cd Flask-Back-end--Productivity-App
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install project dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pipenv install
```

___

# Database Setup

Initialize migrations (only the first time)

```bash
flask db init
```

Generate migration

```bash
flask db migrate -m "Initial migration"
```

Apply migration

```bash
flask db upgrade
```

___

# Seed the Database

Populate the database with sample users and tasks.

```bash
python seed.py
```

___

# Running the Application

Start the Flask server

```bash
flask run
```

or

```bash
python run.py
```

The API will run at

```
http://127.0.0.1:5000
```
___

### API Endpoints
##  Auth Routes
| Method | Endpoint   | Description               | Request Body Example |
|--------|------------|---------------------------|----------------------|
| POST   | /signup    | Register a new user       | { "username": "test", "email": "test@example.com", "password": "password123", "confirm_password": "password123" } |
| POST   | /login     | Login and get JWT token   | { "email": "test@example.com", "password": "password123" } |
| GET    | /me        | Get current user info     | Requires Authorization: Bearer {{access_token}} |
| DELETE | /logout    | Logout (invalidate token) | Requires Authorization: Bearer {{access_token}} |

## Task Routes 
| Method | Endpoint          | Description                  | Request Body Example |
|--------|-------------------|------------------------------|----------------------|
| GET    | /tasks            | Get paginated list of tasks  | Requires Authorization: Bearer {{access_token}} |
| GET    | /tasks/<task_id>  | Get a single task by ID      | Requires Authorization: Bearer {{access_token}} |
| POST   | /tasks            | Create a new task            | { "title": "Sample Task", "content": "This is a test task." } |
| PATCH  | /tasks/<task_id>  | Update an existing task      | { "title": "Updated Task Title" } |
| DELETE | /tasks/<task_id>  | Delete a task                | Requires Authorization: Bearer {{access_token}} |

---

# Example Requests

## Register

```json
POST /signup

{
    "username":"ghost001",
    "password":"123456",
    "password_confirmation":"123456"
}
```

---

## Login

```json
POST /login

{
    "username":"ghost001",
    "password":"123456"
}
```

---

## Create Task

```json
POST /tasks

{
    "title":"Complete Flask Summative",
    "description":"Finish testing all CRUD endpoints",
    "due_date":"2026-08-10"
}
```

---

## Update Task

```json
PATCH /tasks/5

{
    "completed": true
}
```

---

# Example Successful Response

```json
{
    "success": true,
    "data": {
        "task": {
            "id": 5,
            "title": "Complete Flask Summative",
            "description": "Finish testing all CRUD endpoints",
            "completed": true,
            "due_date": "2026-08-10"
        }
    }
}
```

---

# Pagination

Example request

```
GET /tasks?page=1&per_page=10
```

Example response

```json
{
    "success": true,
    "data": {
        "tasks": [],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 0,
            "pages": 0
        }
    }
}
```

---

# Security Features

- Passwords are hashed using Flask-Bcrypt.
- JWT protects all task routes.
- Each task belongs to one authenticated user.
- Users cannot access another user's tasks.
- Unauthorized requests return appropriate HTTP status codes.

---

# Author


Backend Developer

---

# License

For educational purposes 