# API de Gerenciamento de Tarefas

API REST em Flask para criar e acompanhar tarefas, organizada nas camadas Controller, Service e Repository.

## Requisitos

- Python 3.13 ou superior
- SQLite (padrão) ou PostgreSQL

## Instalação e execução

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app.app db upgrade
flask --app app.app run --debug
```

A API fica disponível em `http://127.0.0.1:5000`.

## Configuração

As variáveis aceitas estão em `.env.example`:

- `DATABASE_URL`: conexão SQLAlchemy. O padrão é `sqlite:///tasks.db`.
- `LOG_LEVEL`: nível dos logs, como `INFO` ou `DEBUG`.

Para PostgreSQL, instale um driver compatível e use, por exemplo,
`postgresql+psycopg://usuario:senha@localhost/tasks`.

## Endpoints

| Método | Rota | Função |
|---|---|---|
| POST | `/tasks` | Criar uma tarefa |
| GET | `/tasks` | Listar tarefas |
| GET | `/tasks/{id}` | Buscar uma tarefa |
| PUT | `/tasks/{id}` | Atualizar uma tarefa |
| DELETE | `/tasks/{id}` | Excluir uma tarefa |

### Criar uma tarefa

```json
{
  "titulo": "Preparar relatório",
  "descricao": "Relatório mensal",
  "prioridade": "alta",
  "status": "pendente"
}
```

`prioridade` aceita `baixa`, `média` ou `alta`. `status` aceita `pendente`, `em andamento` ou `concluída`.

### Filtros e paginação

```text
GET /tasks?status=pendente
GET /tasks?prioridade=alta
GET /tasks?status=pendente&prioridade=alta
GET /tasks?page=1&per_page=10
```

Sem paginação, a resposta é uma lista. Com `page` ou `per_page`, a resposta contém `items`, `page`, `per_page`, `total` e `pages`. O máximo é 100 itens por página.

## Regras e respostas

- O título é obrigatório e único.
- A conclusão preenche `data_conclusao` automaticamente.
- Ao sair de `concluída`, a data de conclusão é removida.
- Códigos principais: `200`, `201`, `204`, `400`, `404`, `409` e `500`.

## Testes

```powershell
python -m pytest
```

Os testes usam SQLite em memória e não alteram o banco de desenvolvimento.

## Migrações

Após modificar modelos:

```powershell
flask --app app.app db migrate -m "descricao da alteracao"
flask --app app.app db upgrade
```

## Docker

```powershell
docker build -t tasks-api .
docker run --rm -p 5000:5000 tasks-api
```
