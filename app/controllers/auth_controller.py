from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
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

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({"erro": "Email ou senha inválidos"}), 401
    
    # Gera JWT
    token = jwt.encode({
        "id": usuario.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET, algorithm="HS256")

    return jsonify({
        "mensagem": "Login realizado!",
        "token": token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo
        }
    }), 200
