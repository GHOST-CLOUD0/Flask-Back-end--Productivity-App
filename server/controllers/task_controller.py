from flask import Blueprint, request
from datetime import datetime
from server.models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.extensions import db
from server.utils.responses import success_response, error_response

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data or not data.get('title'):
        return error_response("Title is required.", 400)

    try:
        due_date = None
        if 'due_date' in data and data['due_date']:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            due_date=due_date,
            user_id=user_id
        )

        db.session.add(new_task)
        db.session.commit()

        return success_response({"task": new_task.to_dict()}, 201)
    except ValueError as e:
        return error_response(f"Invalid date format. Use YYYY-MM-DD. {str(e)}", 400)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating task: {str(e)}", 500)

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Task.query.filter_by(user_id=user_id)
    
    total = query.count()
    tasks = query.paginate(page=page, per_page=per_page, error_out=False).items
    tasks_list = [task.to_dict() for task in tasks]

    return success_response({
        "tasks": tasks_list,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }, 200)

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return error_response("Task not found.", 404)

    return success_response({"task": task.to_dict()}, 200)


@task_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
@jwt_required()
def update_task(task_id):
    """Update a task only when it belongs to the authenticated user."""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error_response("Task not found.", 404)

    data = request.get_json(silent=True) or {}
    allowed_fields = {"title", "description", "due_date", "completed"}
    if not data or not any(field in data for field in allowed_fields):
        return error_response("Provide at least one task field to update.", 400)

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return error_response("Title cannot be blank.", 400)
        task.title = data["title"].strip()

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return error_response("Completed must be true or false.", 400)
        task.completed = data["completed"]

    if "due_date" in data:
        try:
            task.due_date = (
                datetime.strptime(data["due_date"], "%Y-%m-%d").date()
                if data["due_date"]
                else None
            )
        except (TypeError, ValueError):
            return error_response("Due date must use YYYY-MM-DD.", 400)

    db.session.commit()
    return success_response({"task": task.to_dict()}, 200)


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task only when it belongs to the authenticated user."""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return error_response("Task not found.", 404)

    db.session.delete(task)
    db.session.commit()
    return "", 204
