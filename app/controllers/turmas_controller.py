from flask import Blueprint, jsonify, request
from app import db
from app.models.turma import Turma
from app.models.curso import Curso

# Blueprint para agrupar as rotas relacionadas às turmas
turmas_bp = Blueprint("turmas", __name__)

# ---------------------------------------------------------
# GET /turmas
# Lista todas as turmas cadastradas
# ---------------------------------------------------------
@turmas_bp.route("/", methods=["GET"])
def listar_turmas():
    turmas = Turma.query.all()

    resultado = []
    for t in turmas:
        resultado.append({
            "id": t.id,
            "nome": t.nome,
            "ano": t.ano,
            "curso_id": t.curso_id,
            "curso": {
                "id": t.curso.id,
                "nome": t.curso.nome,
                "descricao": t.curso.descricao
            }
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /turmas/<id>
# Busca uma turma pelo ID
# ---------------------------------------------------------
@turmas_bp.route("/<int:id>", methods=["GET"])
def buscar_turma(id):
    turma = Turma.query.get(id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    return jsonify({
        "id": turma.id,
        "nome": turma.nome,
        "ano": turma.ano,
        "curso_id": turma.curso_id,
        "curso": {
            "id": turma.curso.id,
            "nome": turma.curso.nome,
            "descricao": turma.curso.descricao
        }
    }), 200


# ---------------------------------------------------------
# POST /turmas
# Cria uma nova turma
# ---------------------------------------------------------
@turmas_bp.route("/", methods=["POST"])

def criar_turma():
    data = request.get_json()

    # Verifica se curso_id foi enviado
    if not data.get("curso_id"):
        return jsonify({"erro": "curso_id é obrigatório"}), 400

    # Verifica se o curso existe
    curso = Curso.query.get(data["curso_id"])
    if not curso:
        return jsonify({"erro": "O curso informado não existe"}), 400

    # Cria nova turma
    nova = Turma(
        curso_id=data["curso_id"],
        nome=data.get("nome"),
        ano=data.get("ano")
    )

    db.session.add(nova)
    db.session.commit()

    return jsonify({"mensagem": "Turma criada com sucesso"}), 201


# ---------------------------------------------------------
# PUT /turmas/<id>
# Atualiza uma turma existente
# ---------------------------------------------------------
# PUT /turmas/<id>
@turmas_bp.route("/<int:id>", methods=["PUT"])
@turmas_bp.route("/<int:id>/", methods=["PUT"])
def atualizar_turma(id):
    turma = Turma.query.get(id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    data = request.get_json()

    turma.nome = data.get("nome", turma.nome)
    turma.ano = data.get("ano", turma.ano)

    if data.get("curso_id"):
        curso = Curso.query.get(data["curso_id"])
        if not curso:
            return jsonify({"erro": "O curso informado não existe"}), 400
        turma.curso_id = data["curso_id"]

    db.session.commit()

    return jsonify({"mensagem": "Turma atualizada com sucesso"}), 200



# ---------------------------------------------------------
# DELETE /turmas/<id>
# Remove uma turma do banco
# ---------------------------------------------------------
@turmas_bp.route("/<int:id>", methods=["DELETE"])
@turmas_bp.route("/<int:id>/", methods=["DELETE"])
def deletar_turma(id):
    turma = Turma.query.get(id)

    if not turma:
        return jsonify({"erro": "Turma não encontrada"}), 404

    db.session.delete(turma)
    db.session.commit()

    return jsonify({"mensagem": "Turma deletada com sucesso"}), 200
