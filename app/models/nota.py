from app import db

# Modelo que representa a tabela "notas"
class Nota(db.Model):
    __tablename__ = "notas"

    id = db.Column(db.Integer, primary_key=True)  # ID da nota
    matricula_id = db.Column(db.Integer, db.ForeignKey("matriculas.id"), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplinas.id"), nullable=False)
    nota = db.Column(db.Numeric(4, 2), nullable=True)  # valor da nota (0.00 a 9999.99)

    # Relacionamentos ORM
    matricula = db.relationship("Matricula", backref="notas")
    disciplina = db.relationship("Disciplina", backref="notas")

    def __repr__(self):
        return f"<Nota {self.id} - {self.nota}>"
