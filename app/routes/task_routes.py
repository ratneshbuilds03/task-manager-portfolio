from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.task_service import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)

task_bp = Blueprint("tasks", __name__)
VALID_STATUSES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}
TASK_FIELDS = {"title", "description", "status", "priority"}


def _validate_task_data(data, partial=False):
    if not isinstance(data, dict):
        return None, "A JSON object is required"
    if not data:
        return None, "At least one task field is required"

    unknown_fields = data.keys() - TASK_FIELDS
    if unknown_fields:
        return None, f"Unsupported field: {sorted(unknown_fields)[0]}"

    validated = {}
    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > 200:
            return None, "title must contain between 1 and 200 characters"
        validated["title"] = title.strip()
    elif not partial:
        return None, "title is required"

    if "description" in data:
        description = data["description"]
        if description is not None and (
            not isinstance(description, str) or len(description) > 5000
        ):
            return None, "description must be a string of at most 5000 characters"
        validated["description"] = description

    if "status" in data:
        status = data["status"]
        if not isinstance(status, str) or status not in VALID_STATUSES:
            return None, "status must be pending, in_progress, or completed"
        validated["status"] = status

    if "priority" in data:
        priority = data["priority"]
        if not isinstance(priority, str) or priority not in VALID_PRIORITIES:
            return None, "priority must be low, medium, or high"
        validated["priority"] = priority

    return validated, None


def _query_integer(name, default, minimum, maximum=None):
    value = request.args.get(name)
    if value is None:
        return default, None
    try:
        parsed = int(value)
    except ValueError:
        return None, f"{name} must be an integer"
    if parsed < minimum or (maximum is not None and parsed > maximum):
        if maximum is None:
            return None, f"{name} must be at least {minimum}"
        return None, f"{name} must be between {minimum} and {maximum}"
    return parsed, None


@task_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def add_task():
    data, error = _validate_task_data(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    task = create_task(data, get_jwt_identity())
    return jsonify(task), 201


@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def list_task():
    user_id = get_jwt_identity()
    status = request.args.get("status")
    priority = request.args.get("priority")
    if status and status not in VALID_STATUSES:
        return jsonify({"error": "Invalid status filter"}), 400
    if priority and priority not in VALID_PRIORITIES:
        return jsonify({"error": "Invalid priority filter"}), 400

    page, error = _query_integer("page", 1, 1)
    if error:
        return jsonify({"error": error}), 400
    per_page, error = _query_integer("per_page", 10, 1, 100)
    if error:
        return jsonify({"error": error}), 400

    result = get_all_tasks(user_id, status, priority, page, per_page)
    return jsonify(result), 200


@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    task = get_task_by_id(task_id, get_jwt_identity())
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def edit_task(task_id):
    data, error = _validate_task_data(request.get_json(silent=True), partial=True)
    if error:
        return jsonify({"error": error}), 400

    task = update_task(task_id, get_jwt_identity(), data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def remove_task(task_id):
    deleted = delete_task(task_id, get_jwt_identity())
    if not deleted:
        return jsonify({"error": "Task not found"}), 404
    return "", 204