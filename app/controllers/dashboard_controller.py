from flask import Blueprint, jsonify
from app.models.aluno import Aluno
from app.models.professor import Professor
from app.models.curso import Curso
from app.models.turma import Turma
from app.models.disciplina import Disciplina
from app.models.arquivo import Arquivo
from app.models.comunicado import Comunicado

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
def dashboard_info():
    return jsonify({
        "total_alunos": Aluno.query.count(),
        "total_professores": Professor.query.count(),
        "total_cursos": Curso.query.count(),
        "total_turmas": Turma.query.count(),
        "total_disciplinas": Disciplina.query.count(),
        "total_arquivos": Arquivo.query.count(),
        "total_comunicados": Comunicado.query.count(),
    })
