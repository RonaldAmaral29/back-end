from app import db

# Modelo que representa a tabela "cursos" no banco de dados
class Curso(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)  # ID do curso
    nome = db.Column(db.String(100), nullable=False)  # Nome do curso (obrigatório)
    descricao = db.Column(db.Text, nullable=True)  # Texto descritivo do curso

    def __repr__(self):
        return f"<Curso {self.id} - {self.nome}>"
