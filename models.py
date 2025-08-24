from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db  = SQLAlchemy()

class Note(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"