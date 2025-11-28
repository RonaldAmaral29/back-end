from app import db

# Modelo que representa a tabela "turmas"
class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)  # ID da turma
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)  # FK para cursos
    nome = db.Column(db.String(50), nullable=True)  # Nome da turma (ex: "Turma A", "3º Ano B")
    ano = db.Column(db.Integer, nullable=True)  # Ano letivo (ex: 2024)

    # Relacionamento com o modelo Curso
    curso = db.relationship("Curso", backref="turmas")

    def __repr__(self):
        return f"<Turma {self.id} - {self.nome}>"
