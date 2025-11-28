from app import db

# Modelo que representa a tabela "disciplinas" no banco de dados
class Disciplina(db.Model):
    __tablename__ = "disciplinas"

    id = db.Column(db.Integer, primary_key=True)  # ID da disciplina
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)  # FK para turmas
    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), nullable=False)  # FK para professores
    nome = db.Column(db.String(100), nullable=False)  # Nome da disciplina

    # Relacionamentos ORM
    turma = db.relationship("Turma", backref="disciplinas")
    professor = db.relationship("Professor", backref="disciplinas")

    def __repr__(self):
        return f"<Disciplina {self.id} - {self.nome}>"
