from flask import Blueprint, jsonify, request
from app.models.curso import Curso
from app import db

# Blueprint para todas as rotas relacionadas aos cursos
cursos_bp = Blueprint("cursos", __name__)

# ---------------------------------------------------------
# GET /cursos
# Lista todos os cursos cadastrados
# ---------------------------------------------------------
@cursos_bp.route("/", methods=["GET"])
def listar_cursos():
    cursos = Curso.query.all()  # Busca todos os cursos

    resultado = []
    for c in cursos:
        resultado.append({
            "id": c.id,
            "nome": c.nome,
            "descricao": c.descricao
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /cursos/<id>
# Busca um curso específico pelo ID
# ---------------------------------------------------------
@cursos_bp.route("/<int:id>", methods=["GET"])
def buscar_curso(id):
    curso = Curso.query.get(id)

    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    return jsonify({
        "id": curso.id,
        "nome": curso.nome,
        "descricao": curso.descricao
    }), 200


# ---------------------------------------------------------
# POST /cursos
# Cria um novo curso
# ---------------------------------------------------------
@cursos_bp.route("", methods=["POST"])
@cursos_bp.route("/", methods=["POST"])
def criar_curso():
    data = request.get_json()

    # Validação do campo obrigatório "nome"
    if not data.get("nome"):
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    # Cria o curso
    novo = Curso(
        nome=data["nome"],
        descricao=data.get("descricao")  # pode ser None
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify({"mensagem": "Curso criado com sucesso"}), 201


# ---------------------------------------------------------
# PUT /cursos/<id>
# Atualiza os dados de um curso já existente
# ---------------------------------------------------------
@cursos_bp.route("/<int:id>", methods=["PUT"])
def atualizar_curso(id):
    curso = Curso.query.get(id)

    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    data = request.get_json()

    # Atualiza os campos enviados
    curso.nome = data.get("nome", curso.nome)
    curso.descricao = data.get("descricao", curso.descricao)

    db.session.commit()

    return jsonify({"mensagem": "Curso atualizado com sucesso"}), 200


# ---------------------------------------------------------
# DELETE /cursos/<id>
# Remove um curso do banco de dados
# ---------------------------------------------------------
@cursos_bp.route("/<int:id>", methods=["DELETE"])
def deletar_curso(id):
    curso = Curso.query.get(id)

    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    db.session.delete(curso)
    db.session.commit()

    return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
