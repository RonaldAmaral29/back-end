from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from werkzeug.security import check_password_hash
import jwt
import datetime
from app import db

auth_bp = Blueprint("auth", __name__)
SECRET = "chave-super-secreta"   # use env em produção

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    # Procurar usuário pelo email
    usuario = Usuario.query.filter_by(email=email).first()

    # Se usuário não existe ou a senha está errada → erro
    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({"erro": "Email ou senha inválidos"}), 401

    # Verifica se o usuário é um aluno
    aluno = Aluno.query.filter_by(usuario_id=usuario.id).first()
    if not aluno:
        return jsonify({"erro": "Apenas alunos podem acessar o sistema"}), 403

    # Gerar o token JWT
    token = jwt.encode({
        "id": usuario.id,
        "tipo": usuario.tipo,
        "aluno_id": aluno.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET, algorithm="HS256")

    return jsonify({
        "mensagem": "Login realizado!",
        "token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "aluno_id": aluno.id
        }
    }), 200
