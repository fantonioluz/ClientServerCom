import json

class classMsgAdd:
    def __init__(self, acao, nome, telefone):
        self.acao = acao
        self.nome = nome
        self.telefone = telefone

    def to_json(self):
        # Serializar o objeto Requisicao para JSON
        return json.dumps({"acao": self.acao, "nome": self.nome, "telefone": self.telefone})
