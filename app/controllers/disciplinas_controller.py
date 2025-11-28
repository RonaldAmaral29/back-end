from flask import Blueprint, jsonify, request
from app import db
from app.models.disciplina import Disciplina
from app.models.turma import Turma
from app.models.professor import Professor

# Blueprint para rotas de disciplinas
disciplinas_bp = Blueprint("disciplinas", __name__)

# ---------------------------------------------------------
# GET /disciplinas
# Lista todas as disciplinas cadastradas
# ---------------------------------------------------------
@disciplinas_bp.route("/", methods=["GET"])
def listar_disciplinas():
    disciplinas = Disciplina.query.all()

    resultado = []
    for d in disciplinas:
        resultado.append({
            "id": d.id,
            "nome": d.nome,
            "turma_id": d.turma_id,
            "professor_id": d.professor_id,
            "turma": {
                "id": d.turma.id,
                "nome": d.turma.nome,
                "ano": d.turma.ano,
                "curso_id": d.turma.curso_id
            },
            "professor": {
                "id": d.professor.id,
                "usuario_id": d.professor.usuario_id,
                "especialidade": d.professor.especialidade
            }
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /disciplinas/<id>
# Busca disciplina por ID
# ---------------------------------------------------------
@disciplinas_bp.route("/<int:id>", methods=["GET"])
def buscar_disciplina(id):
    disciplina = Disciplina.query.get(id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    return jsonify({
        "id": disciplina.id,
        "nome": disciplina.nome,
        "turma_id": disciplina.turma_id,
        "professor_id": disciplina.professor_id,
        "turma": {
            "id": disciplina.turma.id,
            "nome": disciplina.turma.nome,
            "ano": disciplina.turma.ano,
            "curso_id": disciplina.turma.curso_id
        },
        "professor": {
            "id": disciplina.professor.id,
            "usuario_id": disciplina.professor.usuario_id,
            "especialidade": disciplina.professor.especialidade
        }
    }), 200


# ---------------------------------------------------------
# POST /disciplinas
# Cria nova disciplina
# ---------------------------------------------------------
@disciplinas_bp.route("/", methods=["POST"])
def criar_disciplina():
    data = request.get_json()

    # Campos obrigatórios
    campos_obrigatorios = ["turma_id", "professor_id", "nome"]
    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    # Verifica se turma existe
    turma = Turma.query.get(data["turma_id"])
    if not turma:
        return jsonify({"erro": "A turma informada não existe"}), 400

    # Verifica se professor existe
    professor = Professor.query.get(data["professor_id"])
    if not professor:
        return jsonify({"erro": "O professor informado não existe"}), 400

    # Criar disciplina
    nova = Disciplina(
        turma_id=data["turma_id"],
        professor_id=data["professor_id"],
        nome=data["nome"]
    )

    db.session.add(nova)
    db.session.commit()

    return jsonify({"mensagem": "Disciplina criada com sucesso"}), 201


# ---------------------------------------------------------
# PUT /disciplinas/<id>
# Atualiza uma disciplina existente
# ---------------------------------------------------------
@disciplinas_bp.route("/<int:id>", methods=["PUT"])
def atualizar_disciplina(id):
    disciplina = Disciplina.query.get(id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    data = request.get_json()

    # Atualiza nome
    disciplina.nome = data.get("nome", disciplina.nome)

    # Permite trocar turma
    if data.get("turma_id"):
        turma = Turma.query.get(data["turma_id"])
        if not turma:
            return jsonify({"erro": "A turma informada não existe"}), 400
        disciplina.turma_id = data["turma_id"]

    # Permite trocar professor
    if data.get("professor_id"):
        professor = Professor.query.get(data["professor_id"])
        if not professor:
            return jsonify({"erro": "O professor informado não existe"}), 400
        disciplina.professor_id = data["professor_id"]

    db.session.commit()

    return jsonify({"mensagem": "Disciplina atualizada com sucesso"}), 200


# ---------------------------------------------------------
# DELETE /disciplinas/<id>
# Remove disciplina
# ---------------------------------------------------------
@disciplinas_bp.route("/<int:id>", methods=["DELETE"])
def deletar_disciplina(id):
    disciplina = Disciplina.query.get(id)

    if not disciplina:
        return jsonify({"erro": "Disciplina não encontrada"}), 404

    db.session.delete(disciplina)
    db.session.commit()

    return jsonify({"mensagem": "Disciplina deletada com sucesso"}), 200
