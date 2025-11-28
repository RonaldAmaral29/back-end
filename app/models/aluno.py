from app import db

# Modelo da tabela "alunos" no banco de dados
class Aluno(db.Model):
    __tablename__ = "alunos"

    # Colunas
    id = db.Column(db.Integer, primary_key=True)  # ID do aluno
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)  # FK para usuários
    data_nascimento = db.Column(db.Date, nullable=True)  # Data de nascimento

    # Relacionamento ORM (opcional)
    usuario = db.relationship("Usuario", backref="aluno", uselist=False)

    def __repr__(self):
        return f"<Aluno {self.id} - usuario_id={self.usuario_id}>"
