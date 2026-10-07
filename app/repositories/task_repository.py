"""Acesso aos dados das tarefas."""

from app.database import db
from app.models.task import Task


class TaskRepository:
    @staticmethod
    def criar(dados):
        tarefa = Task(**dados)
        db.session.add(tarefa)
        db.session.commit()
        return tarefa

    @staticmethod
    def listar(status=None, prioridade=None, page=None, per_page=None):
        consulta = db.select(Task)
        if status:
            consulta = consulta.where(Task.status == status)
        if prioridade:
            consulta = consulta.where(Task.prioridade == prioridade)
        consulta = consulta.order_by(Task.id)
        if page is not None and per_page is not None:
            return db.paginate(
                consulta, page=page, per_page=per_page, max_per_page=100,
                error_out=False,
            )
        return db.session.scalars(consulta).all()

    @staticmethod
    def buscar_por_id(task_id):
        return db.session.get(Task, task_id)

    @staticmethod
    def buscar_por_titulo(titulo):
        consulta = db.select(Task).where(Task.titulo == titulo)
        return db.session.scalar(consulta)

    @staticmethod
    def atualizar(tarefa, dados):
        for campo, valor in dados.items():
            setattr(tarefa, campo, valor)
        db.session.commit()
        return tarefa

    @staticmethod
    def remover(tarefa):
        db.session.delete(tarefa)
        db.session.commit()
