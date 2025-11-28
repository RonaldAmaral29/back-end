from flask import Flask, request
from flask_cors import CORS
from app import db

def create_app():
    app = Flask(__name__)

    # CONFIGURAÇÕES DO FLASK
    app.config["SECRET_KEY"] = "chave-super-secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    # 🔥 CORRIGE PRÉ-FLIGHT CORS (OPTIONS sempre responde 200)
    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return ("", 200)

    # INICIALIZAR BANCO
    db.init_app(app)

    # IMPORTAR MODELOS
    from app.models.usuario import Usuario
    from app.models.aluno import Aluno
    from app.models.professor import Professor
    from app.models.curso import Curso
    from app.models.turma import Turma
    from app.models.disciplina import Disciplina
    from app.models.matricula import Matricula
    from app.models.nota import Nota
    from app.models.arquivo import Arquivo
    from app.models.comunicado import Comunicado

    with app.app_context():
        db.create_all()

    # REGISTRAR BLUEPRINTS
    from app.controllers.usuarios_controller import usuarios_bp
    from app.controllers.alunos_controller import alunos_bp
    from app.controllers.professores_controller import professores_bp
    from app.controllers.cursos_controller import cursos_bp
    from app.controllers.turmas_controller import turmas_bp
    from app.controllers.disciplinas_controller import disciplinas_bp
    from app.controllers.matriculas_controller import matriculas_bp
    from app.controllers.notas_controller import notas_bp
    from app.controllers.arquivos_controller import arquivos_bp
    from app.controllers.comunicados_controller import comunicados_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.auth_controller import auth_bp

    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(alunos_bp, url_prefix="/alunos")
    app.register_blueprint(professores_bp, url_prefix="/professores")
    app.register_blueprint(cursos_bp, url_prefix="/cursos")
    app.register_blueprint(turmas_bp, url_prefix="/turmas")
    app.register_blueprint(disciplinas_bp, url_prefix="/disciplinas")
    app.register_blueprint(matriculas_bp, url_prefix="/matriculas")
    app.register_blueprint(notas_bp, url_prefix="/notas")
    app.register_blueprint(arquivos_bp, url_prefix="/arquivos")
    app.register_blueprint(comunicados_bp, url_prefix="/comunicados")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)