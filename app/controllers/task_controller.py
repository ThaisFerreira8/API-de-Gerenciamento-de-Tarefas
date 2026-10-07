"""Controllers HTTP das tarefas."""

from flask import jsonify, request
from marshmallow import ValidationError

from app.schemas.task_schema import task_schema, task_update_schema, tasks_schema
from app.services.task_service import (
    TaskNaoEncontradaError,
    TaskService,
    TituloDuplicadoError,
)


def _erro(mensagem, codigo):
    return jsonify({"erro": mensagem}), codigo


def criar_task():
    try:
        dados = task_schema.load(request.get_json(silent=True) or {})
        tarefa = TaskService.criar(dados)
        return jsonify(task_schema.dump(tarefa)), 201
    except ValidationError as erro:
        return _erro(erro.messages, 400)
    except TituloDuplicadoError as erro:
        return _erro(str(erro), 409)


def listar_tasks():
    status = request.args.get("status")
    prioridade = request.args.get("prioridade")
    page_texto = request.args.get("page")
    per_page_texto = request.args.get("per_page")
    try:
        filtros = task_update_schema.load(
            {chave: valor for chave, valor in {
                "status": status,
                "prioridade": prioridade,
            }.items() if valor is not None}
        )
    except ValidationError as erro:
        return _erro(erro.messages, 400)

    page = per_page = None
    if page_texto is not None or per_page_texto is not None:
        try:
            page = int(page_texto or 1)
            per_page = int(per_page_texto or 10)
            if page < 1 or not 1 <= per_page <= 100:
                raise ValueError
        except ValueError:
            return _erro("page deve ser positivo e per_page deve estar entre 1 e 100.", 400)

    tarefas = TaskService.listar(
        filtros.get("status"), filtros.get("prioridade"), page, per_page
    )
    if page is not None:
        return jsonify({
            "items": tasks_schema.dump(tarefas.items),
            "page": tarefas.page,
            "per_page": tarefas.per_page,
            "total": tarefas.total,
            "pages": tarefas.pages,
        }), 200
    return jsonify(tasks_schema.dump(tarefas)), 200


def buscar_task(task_id):
    try:
        return jsonify(task_schema.dump(TaskService.buscar(task_id))), 200
    except TaskNaoEncontradaError as erro:
        return _erro(str(erro), 404)


def atualizar_task(task_id):
    try:
        dados = task_update_schema.load(request.get_json(silent=True) or {})
        if not dados:
            return _erro("Informe ao menos um campo para atualização.", 400)
        tarefa = TaskService.atualizar(task_id, dados)
        return jsonify(task_schema.dump(tarefa)), 200
    except ValidationError as erro:
        return _erro(erro.messages, 400)
    except TaskNaoEncontradaError as erro:
        return _erro(str(erro), 404)
    except TituloDuplicadoError as erro:
        return _erro(str(erro), 409)


def remover_task(task_id):
    try:
        TaskService.remover(task_id)
        return "", 204
    except TaskNaoEncontradaError as erro:
        return _erro(str(erro), 404)
