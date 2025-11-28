from app import db

# Modelo que representa a tabela "professores"
class Professor(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key=True)  # ID do professor
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)  # FK para usuários
    especialidade = db.Column(db.String(100), nullable=True)  # Área de atuação

    # Relacionamento com a tabela de usuários
    usuario = db.relationship("Usuario", backref="professor", uselist=False)

    def __repr__(self):
        return f"<Professor {self.id} - usuario_id={self.usuario_id}>"
