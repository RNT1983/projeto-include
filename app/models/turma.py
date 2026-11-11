from app.extensions import db


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Turma {self.nome}>"
