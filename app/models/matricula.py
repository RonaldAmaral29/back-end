from app import db

# Modelo que representa a tabela "matriculas"
class Matricula(db.Model):
    __tablename__ = "matriculas"

    id = db.Column(db.Integer, primary_key=True)  # ID da matrícula
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)  # FK para alunos
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)  # FK para turmas
    data_matricula = db.Column(db.Date, nullable=True)  # Data da matrícula

    # Relacionamentos ORM
    aluno = db.relationship("Aluno", backref="matriculas")
    turma = db.relationship("Turma", backref="matriculas")

    def __repr__(self):
        return f"<Matricula {self.id} - aluno={self.aluno_id}, turma={self.turma_id}>"
