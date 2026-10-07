def criar_tarefa(client, titulo="Tarefa de teste", **campos):
    dados = {"titulo": titulo, **campos}
    return client.post("/tasks", json=dados)


def test_criar_e_buscar_tarefa(client):
    resposta = criar_tarefa(client, prioridade="alta")
    assert resposta.status_code == 201
    assert resposta.json["status"] == "pendente"
    assert client.get(f"/tasks/{resposta.json['id']}").status_code == 200


def test_titulo_obrigatorio_e_unico(client):
    assert criar_tarefa(client, titulo="").status_code == 400
    assert criar_tarefa(client, titulo="Mesmo título").status_code == 201
    assert criar_tarefa(client, titulo="Mesmo título").status_code == 409


def test_validacao_de_prioridade_e_status(client):
    assert criar_tarefa(client, prioridade="urgente").status_code == 400
    assert criar_tarefa(client, status="cancelada").status_code == 400


def test_listagem_filtros_e_paginacao(client):
    criar_tarefa(client, "Alta", prioridade="alta")
    criar_tarefa(client, "Baixa", prioridade="baixa")
    assert len(client.get("/tasks?prioridade=alta").json) == 1
    resposta = client.get("/tasks?page=1&per_page=1")
    assert resposta.status_code == 200
    assert resposta.json["total"] == 2
    assert len(resposta.json["items"]) == 1
    assert client.get("/tasks?page=0").status_code == 400


def test_data_de_conclusao(client):
    tarefa = criar_tarefa(client).json
    url = f"/tasks/{tarefa['id']}"
    concluida = client.put(url, json={"status": "concluída"})
    assert concluida.json["data_conclusao"] is not None
    pendente = client.put(url, json={"status": "pendente"})
    assert pendente.json["data_conclusao"] is None


def test_atualizar_remover_e_nao_encontrada(client):
    tarefa = criar_tarefa(client).json
    url = f"/tasks/{tarefa['id']}"
    resposta = client.put(url, json={"titulo": "Título atualizado"})
    assert resposta.status_code == 200
    assert resposta.json["titulo"] == "Título atualizado"
    assert client.delete(url).status_code == 204
    assert client.get(url).status_code == 404


def test_put_sem_dados(client):
    tarefa = criar_tarefa(client).json
    assert client.put(f"/tasks/{tarefa['id']}", json={}).status_code == 400
