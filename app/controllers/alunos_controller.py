from flask import Blueprint, jsonify, request
from app import db
from app.models.aluno import Aluno
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime

alunos_bp = Blueprint("alunos", __name__)

# GET /alunos
@alunos_bp.route("/", methods=["GET"])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([
        {
            "id": a.id,
            "data_nascimento": str(a.data_nascimento),
            "usuario": {
                "id": a.usuario.id,
                "nome": a.usuario.nome,
                "email": a.usuario.email,
                "tipo": a.usuario.tipo
            }
        }
        for a in alunos
    ]), 200

# GET /alunos/<id>
@alunos_bp.route("/<int:id>", methods=["GET"])
def buscar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify({
        "id": aluno.id,
        "data_nascimento": str(aluno.data_nascimento),
        "usuario": {
            "id": aluno.usuario.id,
            "nome": aluno.usuario.nome,
            "email": aluno.usuario.email,
            "tipo": aluno.usuario.tipo
        }
    }), 200

# POST /alunos
@alunos_bp.route("/", methods=["POST"])
def criar_aluno():
    data = request.get_json()

    obrigatorios = ["nome", "email", "senha", "data_nascimento"]
    for campo in obrigatorios:
        if not data.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"erro": "O e-mail informado já está cadastrado"}), 400

    usuario = Usuario(
        nome=data["nome"],
        email=data["email"],
        senha_hash=generate_password_hash(data["senha"]),
        tipo="aluno"
    )

    db.session.add(usuario)
    db.session.flush()

    aluno = Aluno(
        usuario_id=usuario.id,
        data_nascimento=datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
    )
    db.session.add(aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno criado com sucesso"}), 201

# PUT /alunos/<id>
@alunos_bp.route("/<int:id>", methods=["PUT"])
def atualizar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    data = request.get_json()

    if data.get("data_nascimento"):
        aluno.data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()

    usuario = aluno.usuario
    usuario.nome = data.get("nome", usuario.nome)
    usuario.email = data.get("email", usuario.email)

    if data.get("senha"):
        usuario.senha_hash = generate_password_hash(data["senha"])

    db.session.commit()
    return jsonify({"mensagem": "Aluno atualizado com sucesso"}), 200

# DELETE /alunos/<id>
@alunos_bp.route("/<int:id>", methods=["DELETE"])
def deletar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    usuario = aluno.usuario

    db.session.delete(aluno)
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensagem": "Aluno deletado com sucesso"}), 200
