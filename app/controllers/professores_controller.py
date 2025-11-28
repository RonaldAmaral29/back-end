from flask import Blueprint, jsonify, request
from app import db
from app.models.professor import Professor
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

# Blueprint dos professores
professores_bp = Blueprint("professores", __name__)


# ---------------------------------------------------------
# GET /professores
# Lista todos os professores com dados do usuário vinculado
# ---------------------------------------------------------
@professores_bp.route("/", methods=["GET"])
def listar_professores():
    professores = Professor.query.all()

    resultado = []

    for p in professores:
        resultado.append({
            "id": p.id,
            "especialidade": p.especialidade,
            "usuario": {
                "id": p.usuario.id,
                "nome": p.usuario.nome,
                "email": p.usuario.email,
                "tipo": p.usuario.tipo
            }
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /professores/<id>
# Dados completos de 1 professor
# ---------------------------------------------------------
@professores_bp.route("/<int:id>", methods=["GET"])
def buscar_professor(id):
    professor = Professor.query.get(id)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    return jsonify({
        "id": professor.id,
        "especialidade": professor.especialidade,
        "usuario": {
            "id": professor.usuario.id,
            "nome": professor.usuario.nome,
            "email": professor.usuario.email,
            "tipo": professor.usuario.tipo
        }
    }), 200


# ---------------------------------------------------------
# POST /professores
# Cria usuário + professor juntos
# ---------------------------------------------------------
@professores_bp.route("/", methods=["POST"])
def criar_professor():
    data = request.get_json()

    # Validação dos campos obrigatórios
    campos_obrigatorios = ["nome", "email", "senha", "especialidade"]
    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    # Verifica se email já existe
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"erro": "O e-mail informado já está cadastrado"}), 400

    # Criar usuário
    novo_usuario = Usuario(
        nome=data["nome"],
        email=data["email"],
        senha_hash=generate_password_hash(data["senha"]),
        tipo="professor"
    )

    db.session.add(novo_usuario)
    db.session.flush()  # Garante que usuario_id exista antes de criar professor

    # Criar professor vinculado ao usuário
    novo_professor = Professor(
        usuario_id=novo_usuario.id,
        especialidade=data["especialidade"]
    )

    db.session.add(novo_professor)
    db.session.commit()

    return jsonify({"mensagem": "Professor criado com sucesso"}), 201


# ---------------------------------------------------------
# PUT /professores/<id>
# Atualiza especialidade e/ou dados do usuário
# ---------------------------------------------------------
@professores_bp.route("/<int:id>", methods=["PUT", "OPTIONS"])
@professores_bp.route("/<int:id>/", methods=["PUT", "OPTIONS"])
def atualizar_professor(id):
    professor = Professor.query.get(id)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    data = request.get_json()

    # Atualizar especialidade
    professor.especialidade = data.get("especialidade", professor.especialidade)

    # Atualizar dados do usuário vinculado
    usuario = professor.usuario

    usuario.nome = data.get("nome", usuario.nome)
    usuario.email = data.get("email", usuario.email)

    if data.get("senha"):
        usuario.senha_hash = generate_password_hash(data["senha"])

    db.session.commit()

    return jsonify({"mensagem": "Professor atualizado com sucesso"}), 200


# ---------------------------------------------------------
# DELETE /professores/<id>
# Remove professor + usuário juntos
# ---------------------------------------------------------
@professores_bp.route("/<int:id>", methods=["DELETE", "OPTIONS"])
@professores_bp.route("/<int:id>/", methods=["DELETE", "OPTIONS"])
def deletar_professor(id):
    professor = Professor.query.get(id)

    if not professor:
        return jsonify({"erro": "Professor não encontrado"}), 404

    usuario = professor.usuario

    db.session.delete(professor)
    db.session.delete(usuario)  # Remove o usuário vinculado
    db.session.commit()

    return jsonify({"mensagem": "Professor deletado com sucesso"}), 200
