from app.extensions import db


class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    turma_id = db.Column(
        db.Integer,
        db.ForeignKey("turmas.id"),
        nullable=True
    )

    turma = db.relationship("Turma", backref="alunos")

    def __repr__(self):
        return f"<Aluno {self.nome}>"
