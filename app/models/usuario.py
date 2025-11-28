from app import db

# Modelo que representa a tabela "usuarios" no banco de dados.
class Usuario(db.Model):
    __tablename__ = "usuarios"  # Nome real da tabela no SQLite

    # Campos / colunas do banco
    id = db.Column(db.Integer, primary_key=True)  # ID único
    nome = db.Column(db.String(100), nullable=False)  # Nome do usuário
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email único
    senha_hash = db.Column(db.String(255), nullable=False)  # Senha já criptografada
    tipo = db.Column(db.String(20), nullable=False)  # admin / professor / aluno

    # Método auxiliar (útil para debug, logs, etc.)
    def __repr__(self):
        return f"<Usuario {self.id} - {self.nome}>"
