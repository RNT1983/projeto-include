
from app.extensions import db


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    curso_id = db.Column(
        db.Integer,
        db.ForeignKey("cursos.id"),
        nullable=True
    )

    curso = db.relationship("Curso", backref="turmas")

    def __repr__(self):
        return f"<Turma {self.nome}>"
