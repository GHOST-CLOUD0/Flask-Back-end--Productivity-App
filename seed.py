from datetime import date

from app import app
from server.extensions import db
from server.models.task import Task
from server.models.user import User


SAMPLE_USERS = [
    {
        "username": "ada",
        "password": "ada-password",
        "tasks": [
            {"title": "Plan weekly goals", "description": "Set three priorities.", "due_date": date(2026, 8, 7)},
            {"title": "Review inbox", "description": "Clear outstanding messages.", "completed": True},
        ],
    },
    {
        "username": "sam",
        "password": "sam-password",
        "tasks": [
            {"title": "Write project notes", "description": "Summarize today's progress."},
            {"title": "Schedule focus time", "description": "Block two hours on the calendar."},
        ],
    },
]


def seed_database():
    """Create example users and tasks without deleting existing records."""
    for user_data in SAMPLE_USERS:
        user = User.query.filter_by(username=user_data["username"]).first()
        if user is None:
            user = User(username=user_data["username"])
            user.password = user_data["password"]
            db.session.add(user)
            db.session.flush()

        for task_data in user_data["tasks"]:
            exists = Task.query.filter_by(user_id=user.id, title=task_data["title"]).first()
            if exists is None:
                db.session.add(Task(user_id=user.id, **task_data))

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed_database()
    print("Database seeded successfully.")