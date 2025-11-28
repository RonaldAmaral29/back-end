from app import db
from datetime import datetime

# Modelo que representa a tabela "arquivos"
class Arquivo(db.Model):
    __tablename__ = "arquivos"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=True)
    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), nullable=True)
    nome = db.Column(db.String(255), nullable=False)  # nome original do arquivo
    caminho = db.Column(db.String(255), nullable=False)  # caminho salvo no servidor
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos ORM
    aluno = db.relationship("Aluno", backref="arquivos")
    professor = db.relationship("Professor", backref="arquivos")

    def __repr__(self):
        return f"<Arquivo {self.id} - {self.nome}>"
