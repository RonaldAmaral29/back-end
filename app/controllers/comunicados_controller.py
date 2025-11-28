from flask import Blueprint, jsonify, request
from app import db
from app.models.comunicado import Comunicado

# Blueprint para as rotas de comunicados
comunicados_bp = Blueprint("comunicados", __name__)

# ---------------------------------------------------------
# GET /comunicados
# Lista todos os comunicados
# ---------------------------------------------------------
@comunicados_bp.route("/", methods=["GET"])
def listar_comunicados():
    comunicados = Comunicado.query.all()

    resultado = []
    for c in comunicados:
        resultado.append({
            "id": c.id,
            "titulo": c.titulo,
            "conteudo": c.conteudo,
            "data_publicacao": str(c.data_publicacao)
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /comunicados/<id>
# Busca um comunicado específico
# ---------------------------------------------------------
@comunicados_bp.route("/<int:id>", methods=["GET"])
def buscar_comunicado(id):
    comunicado = Comunicado.query.get(id)

    if not comunicado:
        return jsonify({"erro": "Comunicado não encontrado"}), 404

    return jsonify({
        "id": comunicado.id,
        "titulo": comunicado.titulo,
        "conteudo": comunicado.conteudo,
        "data_publicacao": str(comunicado.data_publicacao)
    }), 200


# ---------------------------------------------------------
# POST /comunicados
# Cria um novo comunicado
# ---------------------------------------------------------
@comunicados_bp.route("/", methods=["POST"])
def criar_comunicado():
    data = request.get_json()

    # Validação do campo obrigatório
    if not data.get("titulo"):
        return jsonify({"erro": "O campo 'titulo' é obrigatório"}), 400

    novo = Comunicado(
        titulo=data["titulo"],
        conteudo=data.get("conteudo"),
        data_publicacao=data.get("data_publicacao")
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Comunicado criado com sucesso"}), 201


# ---------------------------------------------------------
# PUT /comunicados/<id>
# Atualiza um comunicado existente
# ---------------------------------------------------------
@comunicados_bp.route("/<int:id>", methods=["PUT"])
def atualizar_comunicado(id):
    comunicado = Comunicado.query.get(id)

    if not comunicado:
        return jsonify({"erro": "Comunicado não encontrado"}), 404

    data = request.get_json()

    # Atualiza apenas os campos enviados
    comunicado.titulo = data.get("titulo", comunicado.titulo)
    comunicado.conteudo = data.get("conteudo", comunicado.conteudo)
    comunicado.data_publicacao = data.get("data_publicacao", comunicado.data_publicacao)

    db.session.commit()

    return jsonify({"mensagem": "Comunicado atualizado com sucesso"}), 200


# ---------------------------------------------------------
# DELETE /comunicados/<id>
# Remove um comunicado do banco
# ---------------------------------------------------------
@comunicados_bp.route("/<int:id>", methods=["DELETE"])
def deletar_comunicado(id):
    comunicado = Comunicado.query.get(id)

    if not comunicado:
        return jsonify({"erro": "Comunicado não encontrado"}), 404

    db.session.delete(comunicado)
    db.session.commit()

    return jsonify({"mensagem": "Comunicado deletado com sucesso"}), 200
