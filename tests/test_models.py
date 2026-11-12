from app import create_app
from app.extensions import db
from app.models import Aluno, Turma


def test_criar_e_consultar_aluno(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

        turma = Turma(nome="Turma de Teste")
        db.session.add(turma)
        db.session.commit()

        aluno = Aluno(nome="Aluno de Teste", turma_id=turma.id)
        db.session.add(aluno)
        db.session.commit()

        aluno_consultado = db.session.get(Aluno, aluno.id)

        assert aluno_consultado is not None
        assert aluno_consultado.nome == "Aluno de Teste"
        assert aluno_consultado.turma.nome == "Turma de Teste"

        db.session.remove()
        db.drop_all()