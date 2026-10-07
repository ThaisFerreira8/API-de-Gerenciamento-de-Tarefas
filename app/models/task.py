"""Modelo de uma tarefa."""

from datetime import datetime, timezone

from app.database import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False, unique=True, index=True)
    descricao = db.Column(db.Text, nullable=True)
    prioridade = db.Column(db.String(10), nullable=False, default="baixa")
    status = db.Column(db.String(20), nullable=False, default="pendente")
    data_criacao = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    data_conclusao = db.Column(db.DateTime(timezone=True), nullable=True)
