
from app.extensions import db


class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    responsavel = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)

    # Informações opcionais sobre o perfil do aluno
    deficiencia_fisica = db.Column(db.Boolean, nullable=True)
    deficiencia_intelectual = db.Column(db.Boolean, nullable=True)
    tea = db.Column(db.Boolean, nullable=True)
    recebe_beneficio = db.Column(db.Boolean, nullable=True)
    tipo_beneficio = db.Column(db.String(120), nullable=True)

    ativo = db.Column(db.Boolean, default=True, nullable=False)

    turma_id = db.Column(
        db.Integer,
        db.ForeignKey("turmas.id"),
        nullable=True
    )

    turma = db.relationship("Turma", backref="alunos")

    def __repr__(self):
        return f"<Aluno {self.nome}>"
