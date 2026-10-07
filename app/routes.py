"""Registro central das rotas da API."""

from flask import Blueprint, jsonify

from app.controllers.task_controller import (
    atualizar_task,
    buscar_task,
    criar_task,
    listar_tasks,
    remover_task,
)


api = Blueprint("api", __name__)


@api.get("/")
def health_check():
    """Confirma que a API está em execução."""
    return jsonify({"mensagem": "API de Gerenciamento de Tarefas"}), 200


api.add_url_rule("/tasks", view_func=criar_task, methods=["POST"])
api.add_url_rule("/tasks", view_func=listar_tasks, methods=["GET"])
api.add_url_rule("/tasks/<int:task_id>", view_func=buscar_task, methods=["GET"])
api.add_url_rule("/tasks/<int:task_id>", view_func=atualizar_task, methods=["PUT"])
api.add_url_rule("/tasks/<int:task_id>", view_func=remover_task, methods=["DELETE"])
