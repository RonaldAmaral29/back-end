from app import db

# Modelo que representa a tabela "comunicados"
class Comunicado(db.Model):
    __tablename__ = "comunicados"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)  # título do comunicado
    conteudo = db.Column(db.Text, nullable=True)        # texto do comunicado
    data_publicacao = db.Column(db.Date, nullable=True) # data do comunicado

    def __repr__(self):
        return f"<Comunicado {self.id} - {self.titulo}>"
