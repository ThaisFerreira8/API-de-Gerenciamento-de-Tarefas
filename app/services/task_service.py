"""Regras de negócio das tarefas."""

from datetime import datetime, timezone

from app.repositories.task_repository import TaskRepository


class TaskNaoEncontradaError(Exception):
    pass


class TituloDuplicadoError(Exception):
    pass


class TaskService:
    @staticmethod
    def criar(dados):
        dados["titulo"] = dados["titulo"].strip()
        if TaskRepository.buscar_por_titulo(dados["titulo"]):
            raise TituloDuplicadoError("Já existe uma tarefa com esse título.")
        if dados.get("status") == "concluída":
            dados["data_conclusao"] = datetime.now(timezone.utc)
        return TaskRepository.criar(dados)

    @staticmethod
    def listar(status=None, prioridade=None, page=None, per_page=None):
        return TaskRepository.listar(status, prioridade, page, per_page)

    @staticmethod
    def buscar(task_id):
        tarefa = TaskRepository.buscar_por_id(task_id)
        if not tarefa:
            raise TaskNaoEncontradaError("Tarefa não encontrada.")
        return tarefa

    @staticmethod
    def atualizar(task_id, dados):
        tarefa = TaskService.buscar(task_id)

        if "titulo" in dados:
            dados["titulo"] = dados["titulo"].strip()
            existente = TaskRepository.buscar_por_titulo(dados["titulo"])
            if existente and existente.id != tarefa.id:
                raise TituloDuplicadoError("Já existe uma tarefa com esse título.")

        if "status" in dados:
            if dados["status"] == "concluída" and tarefa.status != "concluída":
                dados["data_conclusao"] = datetime.now(timezone.utc)
            elif dados["status"] != "concluída":
                dados["data_conclusao"] = None

        return TaskRepository.atualizar(tarefa, dados)

    @staticmethod
    def remover(task_id):
        tarefa = TaskService.buscar(task_id)
        TaskRepository.remover(tarefa)
