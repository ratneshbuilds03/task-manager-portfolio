from app import db
from app.models.task import Task

def create_task(data, user_id):
    new_task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        user_id=user_id,
    )
    db.session.add(new_task)
    db.session.commit()
    return new_task.to_dict()

def get_all_tasks(user_id, status=None, priority=None, page=1, per_page=10):
    query = Task.query.filter_by(user_id=user_id)

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    pagination = query.order_by(Task.created_at.desc(), Task.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return {
        "tasks": [task.to_dict() for task in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    }


def get_task_by_id(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    return task.to_dict() if task else None


def update_task(task_id, user_id, data):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return None

    for field, value in data.items():
        setattr(task, field, value)
    db.session.commit()
    return task.to_dict()


def delete_task(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return False

    db.session.delete(task)
    db.session.commit()
    return True
