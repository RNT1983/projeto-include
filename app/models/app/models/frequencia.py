from datetime import date

from app.extensions import db


class Frequencia(db.Model):
    __tablename__ = "frequencias"

    id = db.Column(db.Integer, primary_key=True)

    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey("alunos.id"),
        nullable=False
    )

    data = db.Column(db.Date, default=date.today, nullable=False)

    presente = db.Column(db.Boolean, nullable=False)

    observacao = db.Column(db.String(255), nullable=True)

    aluno = db.relationship("Aluno", backref="frequencias")

    def __repr__(self):
        return f"<Frequencia {self.aluno_id} - {self.data}>"
