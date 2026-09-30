from app import db
from datetime import datetime, timezone

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.Text,nullable=True)
    status = db.Column(db.String(20),default="pending")
    priority = db.Column(db.String(10),default="medium")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def to_dict(self):
        return{
            "id":self.id ,
            "title":self.title ,
            "description":self.description ,
            "status":self.status ,
            "priority":self.priority ,
            "created_at":self.created_at,
            "user_id":self.user_id
            }
