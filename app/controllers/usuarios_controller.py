from flask import Blueprint, jsonify, request
from app.models.usuario import Usuario
from app import db

# Blueprint para agrupar todas as rotas relacionadas aos usuários
usuarios_bp = Blueprint("usuarios", __name__)

# -----------------------------------------
# GET /usuarios
# Lista todos os usuários cadastrados
# -----------------------------------------
@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()  # Buscar todos no banco

    # Constrói uma lista de objetos JSON para retornar
    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "tipo": u.tipo
        })

    return jsonify(resultado), 200


# -----------------------------------------
# GET /usuarios/<id>
# Busca um usuário específico pelo ID
# -----------------------------------------
@usuarios_bp.route("/<int:id>", methods=["GET"])
def buscar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo
    }), 200


# -----------------------------------------
# POST /usuarios
# Cria um novo usuário
# -----------------------------------------
@usuarios_bp.route("/", methods=["POST"])
def criar_usuario():
    data = request.get_json()  # Recebe JSON enviado pelo frontend

    # Validações simples
    if not data.get("nome") or not data.get("email") or not data.get("senha_hash") or not data.get("tipo"):
        return jsonify({"erro": "Dados incompletos"}), 400

    # Cria o objeto no ORM
    novo = Usuario(
        nome=data["nome"],
        email=data["email"],
        senha_hash=data["senha_hash"],  # já deve vir criptografado
        tipo=data["tipo"]
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso"}), 201


# -----------------------------------------
# PUT /usuarios/<id>
# Atualiza os dados de um usuário existente
# -----------------------------------------
@usuarios_bp.route("/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    data = request.get_json()

    # Atualiza apenas os campos enviados
    usuario.nome = data.get("nome", usuario.nome)
    usuario.email = data.get("email", usuario.email)
    usuario.tipo = data.get("tipo", usuario.tipo)

    db.session.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200


# -----------------------------------------
# DELETE /usuarios/<id>
# Remove um usuário do banco
# -----------------------------------------
@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
