"""Validação e serialização de tarefas."""

from marshmallow import Schema, ValidationError, fields, validate, validates


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=1, max=150))
    descricao = fields.String(allow_none=True)
    prioridade = fields.String(
        load_default="baixa",
        validate=validate.OneOf(["baixa", "média", "alta"]),
    )
    status = fields.String(
        load_default="pendente",
        validate=validate.OneOf(["pendente", "em andamento", "concluída"]),
    )
    data_criacao = fields.DateTime(dump_only=True)
    data_conclusao = fields.DateTime(dump_only=True, allow_none=True)

    @validates("titulo")
    def validar_titulo(self, valor, **kwargs):
        if not valor.strip():
            raise ValidationError("O título é obrigatório.")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_update_schema = TaskSchema(partial=True)
