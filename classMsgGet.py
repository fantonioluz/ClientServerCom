import json

#dois tipos de msg
#add = acao, nome, telefone
#pesquisar = acao, nome

#a msg é mandada em formato de d=objeto para serializar me json e enviar
class classMsgGet:
    def __init__(self, acao, nome):
        self.acao = acao
        self.nome = nome

#ent a msg obj tem a função de ser transf p json
    def to_json(self):
        # Serializar o objeto Requisicao para JSON
        return json.dumps({"acao": self.acao, "nome": self.nome})
