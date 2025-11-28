from flask import Blueprint, jsonify, request
from app import db
from app.models.matricula import Matricula
from app.models.aluno import Aluno
from app.models.turma import Turma

# Blueprint para as rotas de matrículas
matriculas_bp = Blueprint("matriculas", __name__)

# ---------------------------------------------------------
# GET /matriculas
# Lista todas as matrículas cadastradas
# ---------------------------------------------------------
@matriculas_bp.route("/", methods=["GET"])
def listar_matriculas():
    matriculas = Matricula.query.all()

    resultado = []
    for m in matriculas:
        resultado.append({
            "id": m.id,
            "aluno_id": m.aluno_id,
            "turma_id": m.turma_id,
            "data_matricula": str(m.data_matricula),
            "aluno": {
                "id": m.aluno.id,
                "usuario_id": m.aluno.usuario_id,
                "data_nascimento": str(m.aluno.data_nascimento)
            },
            "turma": {
                "id": m.turma.id,
                "nome": m.turma.nome,
                "ano": m.turma.ano,
                "curso_id": m.turma.curso_id
            }
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /matriculas/<id>
# Busca matrícula específica
# ---------------------------------------------------------
@matriculas_bp.route("/<int:id>", methods=["GET"])
def buscar_matricula(id):
    matricula = Matricula.query.get(id)

    if not matricula:
        return jsonify({"erro": "Matrícula não encontrada"}), 404

    return jsonify({
        "id": matricula.id,
        "aluno_id": matricula.aluno_id,
        "turma_id": matricula.turma_id,
        "data_matricula": str(matricula.data_matricula),
        "aluno": {
            "id": matricula.aluno.id,
            "usuario_id": matricula.aluno.usuario_id,
            "data_nascimento": str(matricula.aluno.data_nascimento)
        },
        "turma": {
            "id": matricula.turma.id,
            "nome": matricula.turma.nome,
            "ano": matricula.turma.ano,
            "curso_id": matricula.turma.curso_id
        }
    }), 200


# ---------------------------------------------------------
# POST /matriculas
# Cria uma nova matrícula
# ---------------------------------------------------------
@matriculas_bp.route("/", methods=["POST"])
def criar_matricula():
    data = request.get_json()

    # Verificação dos campos obrigatórios
    obrigatorios = ["aluno_id", "turma_id"]
    for campo in obrigatorios:
        if not data.get(campo):
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    # Verificar existência do aluno
    aluno = Aluno.query.get(data["aluno_id"])
    if not aluno:
        return jsonify({"erro": "O aluno informado não existe"}), 400

    # Verificar existência da turma
    turma = Turma.query.get(data["turma_id"])
    if not turma:
        return jsonify({"erro": "A turma informada não existe"}), 400

    # Criar matrícula
    nova = Matricula(
        aluno_id=data["aluno_id"],
        turma_id=data["turma_id"],
        data_matricula=data.get("data_matricula")
    )

    db.session.add(nova)
    db.session.commit()

    return jsonify({"mensagem": "Matrícula criada com sucesso"}), 201


# ---------------------------------------------------------
# PUT /matriculas/<id>
# Atualiza uma matrícula existente
# ---------------------------------------------------------
@matriculas_bp.route("/<int:id>", methods=["PUT"])
def atualizar_matricula(id):
    matricula = Matricula.query.get(id)

    if not matricula:
        return jsonify({"erro": "Matrícula não encontrada"}), 404

    data = request.get_json()

    # Atualizar data de matrícula
    matricula.data_matricula = data.get("data_matricula", matricula.data_matricula)

    # Atualizar aluno (opcional)
    if data.get("aluno_id"):
        aluno = Aluno.query.get(data["aluno_id"])
        if not aluno:
            return jsonify({"erro": "O aluno informado não existe"}), 400
        matricula.aluno_id = data["aluno_id"]

    # Atualizar turma (opcional)
    if data.get("turma_id"):
        turma = Turma.query.get(data["turma_id"])
        if not turma:
            return jsonify({"erro": "A turma informada não existe"}), 400
        matricula.turma_id = data["turma_id"]

    db.session.commit()

    return jsonify({"mensagem": "Matrícula atualizada com sucesso"}), 200


# ---------------------------------------------------------
# DELETE /matriculas/<id>
# Remove uma matrícula do banco
# ---------------------------------------------------------
@matriculas_bp.route("/<int:id>", methods=["DELETE"])
def deletar_matricula(id):
    matricula = Matricula.query.get(id)

    if not matricula:
        return jsonify({"erro": "Matrícula não encontrada"}), 404

    db.session.delete(matricula)
    db.session.commit()

    return jsonify({"mensagem": "Matrícula deletada com sucesso"}), 200
