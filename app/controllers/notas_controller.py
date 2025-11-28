from flask import Blueprint, jsonify, request
from app import db
from app.models.nota import Nota
from app.models.matricula import Matricula
from app.models.disciplina import Disciplina

# Blueprint para rotas de notas
notas_bp = Blueprint("notas", __name__)

# ---------------------------------------------------------
# GET /notas
# Lista todas as notas cadastradas
# ---------------------------------------------------------
@notas_bp.route("/", methods=["GET"])
def listar_notas():
    notas = Nota.query.all()

    resultado = []
    for n in notas:
        resultado.append({
            "id": n.id,
            "nota": float(n.nota) if n.nota is not None else None,
            "matricula_id": n.matricula_id,
            "disciplina_id": n.disciplina_id,

            # Dados completos da matrícula
            "matricula": {
                "id": n.matricula.id,
                "aluno_id": n.matricula.aluno_id,
                "turma_id": n.matricula.turma_id,
                "data_matricula": str(n.matricula.data_matricula)
            },

            # Dados completos da disciplina
            "disciplina": {
                "id": n.disciplina.id,
                "nome": n.disciplina.nome,
                "turma_id": n.disciplina.turma_id,
                "professor_id": n.disciplina.professor_id
            }
        })

    return jsonify(resultado), 200


# ---------------------------------------------------------
# GET /notas/<id>
# Busca uma nota específica
# ---------------------------------------------------------
@notas_bp.route("/<int:id>", methods=["GET"])
def buscar_nota(id):
    nota = Nota.query.get(id)

    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404

    return jsonify({
        "id": nota.id,
        "nota": float(nota.nota) if nota.nota is not None else None,
        "matricula_id": nota.matricula_id,
        "disciplina_id": nota.disciplina_id,

        "matricula": {
            "id": nota.matricula.id,
            "aluno_id": nota.matricula.aluno_id,
            "turma_id": nota.matricula.turma_id,
            "data_matricula": str(nota.matricula.data_matricula)
        },

        "disciplina": {
            "id": nota.disciplina.id,
            "nome": nota.disciplina.nome,
            "turma_id": nota.disciplina.turma_id,
            "professor_id": nota.disciplina.professor_id
        }
    }), 200


# ---------------------------------------------------------
# POST /notas
# Cria uma nova nota
# ---------------------------------------------------------
@notas_bp.route("/", methods=["POST"])
def criar_nota():
    data = request.get_json()

    # Campos obrigatórios
    obrigatorios = ["matricula_id", "disciplina_id", "nota"]
    for campo in obrigatorios:
        if campo not in data:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório"}), 400

    # Validar existência da matrícula
    matricula = Matricula.query.get(data["matricula_id"])
    if not matricula:
        return jsonify({"erro": "A matrícula informada não existe"}), 400

    # Validar existência da disciplina
    disciplina = Disciplina.query.get(data["disciplina_id"])
    if not disciplina:
        return jsonify({"erro": "A disciplina informada não existe"}), 400

    # Validar nota
    try:
        valor_nota = float(data["nota"])
        if valor_nota < 0 or valor_nota > 10:
            return jsonify({"erro": "A nota deve estar entre 0 e 10"}), 400
    except:
        return jsonify({"erro": "A nota deve ser um número válido"}), 400

    nova = Nota(
        matricula_id=data["matricula_id"],
        disciplina_id=data["disciplina_id"],
        nota=valor_nota
    )

    db.session.add(nova)
    db.session.commit()

    return jsonify({"mensagem": "Nota criada com sucesso"}), 201


# ---------------------------------------------------------
# PUT /notas/<id>
# Atualiza uma nota existente
# ---------------------------------------------------------
@notas_bp.route("/<int:id>", methods=["PUT"])
def atualizar_nota(id):
    nota = Nota.query.get(id)

    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404

    data = request.get_json()

    # Atualizar nota
    if "nota" in data:
        try:
            valor_nota = float(data["nota"])
            if valor_nota < 0 or valor_nota > 10:
                return jsonify({"erro": "A nota deve estar entre 0 e 10"}), 400
            nota.nota = valor_nota
        except:
            return jsonify({"erro": "A nota deve ser numérica"}), 400

    # Atualizar matricula (opcional)
    if data.get("matricula_id"):
        matricula = Matricula.query.get(data["matricula_id"])
        if not matricula:
            return jsonify({"erro": "A matrícula informada não existe"}), 400
        nota.matricula_id = data["matricula_id"]

    # Atualizar disciplina (opcional)
    if data.get("disciplina_id"):
        disciplina = Disciplina.query.get(data["disciplina_id"])
        if not disciplina:
            return jsonify({"erro": "A disciplina informada não existe"}), 400
        nota.disciplina_id = data["disciplina_id"]

    db.session.commit()

    return jsonify({"mensagem": "Nota atualizada com sucesso"}), 200


# ---------------------------------------------------------
# DELETE /notas/<id>
# Remove uma nota
# ---------------------------------------------------------
@notas_bp.route("/<int:id>", methods=["DELETE"])
def deletar_nota(id):
    nota = Nota.query.get(id)

    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404

    db.session.delete(nota)
    db.session.commit()

    return jsonify({"mensagem": "Nota deletada com sucesso"}), 200
