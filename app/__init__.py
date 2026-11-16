
import os
import hmac
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from app.extensions import db


def create_app():
    app = Flask(__name__)

    # Reconhece o HTTPS encaminhado pelo proxy do GitHub Codespaces.
    # Usar somente atrás de um proxy confiável.
    app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)

    # Configuração da chave de segurança da aplicação.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Configuração do banco de dados.
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///projeto_include.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Proteção CSRF ativada para requisições POST.
    app.config["WTF_CSRF_ENABLED"] = True
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Inicializa o banco de dados.
    db.init_app(app)

    from app.models import Aluno, Turma, Frequencia, Curso

    with app.app_context():
        db.create_all()

    # Verifica se o administrador está autenticado.
    def login_obrigatorio(funcao):
        @wraps(funcao)
        def verificar_acesso(*args, **kwargs):
            if not session.get("admin_autenticado"):

                # Guarda somente o caminho de páginas acessadas via GET.
                # Não reutiliza requisições POST após o login.
                if request.method == "GET":
                    session["pagina_destino"] = request.full_path.rstrip("?")
                else:
                    session["pagina_destino"] = url_for("index")

                return redirect(url_for("login"))

            return funcao(*args, **kwargs)

        return verificar_acesso

    # LOGIN ADMINISTRATIVO
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            senha_informada = request.form.get("senha", "")
            senha_configurada = os.environ.get("ADMIN_PASSWORD")

            if senha_configurada and hmac.compare_digest(
                senha_informada, senha_configurada
            ):
                # Recupera a página solicitada antes de limpar a sessão.
                pagina_destino = session.get(
                    "pagina_destino",
                    url_for("index")
                )

                # Aceita apenas caminhos internos.
                if (
                    not isinstance(pagina_destino, str)
                    or not pagina_destino.startswith("/")
                    or pagina_destino.startswith("//")
                    or "\\" in pagina_destino
                ):
                    pagina_destino = url_for("index")

                session.clear()
                session["admin_autenticado"] = True

                return redirect(pagina_destino)

            return render_template(
                "login.html",
                erro="Senha incorreta."
            ), 401

        return render_template("login.html")

    # ENCERRAR SESSÃO ADMINISTRATIVA
    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return redirect(url_for("index"))

    # Converte as opções dos formulários em valores booleanos.
    def valor_booleano(campo):
        valor = request.form.get(campo, "")

        if valor == "sim":
            return True
        elif valor == "nao":
            return False

        return None

    # PÁGINA INICIAL
    @app.route("/")
    def index():
        return render_template("index.html")

    # CADASTRO E CONSULTA DE ALUNOS
    @app.route("/alunos", methods=["GET", "POST"])
    @login_obrigatorio
    def alunos():
        if request.method == "POST":
            novo_aluno = Aluno(
                nome=request.form["nome"],
                idade=int(request.form["idade"]),
                responsavel=request.form["responsavel"],
                cpf=request.form.get("cpf") or None,
                endereco=request.form.get("endereco") or None,
                deficiencia_fisica=valor_booleano("deficiencia_fisica"),
                deficiencia_intelectual=valor_booleano("deficiencia_intelectual"),
                tea=valor_booleano("tea"),
                recebe_beneficio=valor_booleano("recebe_beneficio"),
                tipo_beneficio=request.form.get("tipo_beneficio") or None
            )

            db.session.add(novo_aluno)
            db.session.commit()

            return redirect(url_for("alunos"))

        lista_alunos = Aluno.query.filter_by(ativo=True).all()

        return render_template("alunos.html", alunos=lista_alunos)

    # EDIÇÃO DE ALUNOS
    @app.route("/alunos/editar/<int:id>", methods=["GET", "POST"])
    @login_obrigatorio
    def editar_aluno(id):
        aluno = db.session.get(Aluno, id)

        if aluno is None or not aluno.ativo:
            return redirect(url_for("alunos"))

        if request.method == "POST":
            aluno.nome = request.form["nome"]
            aluno.idade = int(request.form["idade"])
            aluno.responsavel = request.form["responsavel"]
            aluno.cpf = request.form.get("cpf") or None
            aluno.endereco = request.form.get("endereco") or None

            aluno.deficiencia_fisica = valor_booleano("deficiencia_fisica")
            aluno.deficiencia_intelectual = valor_booleano("deficiencia_intelectual")
            aluno.tea = valor_booleano("tea")
            aluno.recebe_beneficio = valor_booleano("recebe_beneficio")
            aluno.tipo_beneficio = request.form.get("tipo_beneficio") or None

            db.session.commit()

            return redirect(url_for("alunos"))

        return render_template("editar_aluno.html", aluno=aluno)

    # EXCLUSÃO LÓGICA DE ALUNOS
    @app.route("/alunos/excluir/<int:id>", methods=["POST"])
    @login_obrigatorio
    def excluir_aluno(id):
        aluno = db.session.get(Aluno, id)

        if aluno is not None:
            aluno.ativo = False
            db.session.commit()

        return redirect(url_for("alunos"))

    # CADASTRO E CONSULTA DE CURSOS
    @app.route("/cursos", methods=["GET", "POST"])
    @login_obrigatorio
    def cursos():
        if request.method == "POST":
            novo_curso = Curso(
                nome=request.form["nome"],
                descricao=request.form.get("descricao") or None,
                carga_horaria=int(request.form["carga_horaria"])
                if request.form.get("carga_horaria") else None
            )

            db.session.add(novo_curso)
            db.session.commit()

            return redirect(url_for("cursos"))

        lista_cursos = Curso.query.filter_by(ativo=True).all()

        return render_template("cursos.html", cursos=lista_cursos)

    # EDIÇÃO DE CURSOS
    @app.route("/cursos/editar/<int:id>", methods=["GET", "POST"])
    @login_obrigatorio
    def editar_curso(id):
        curso = db.session.get(Curso, id)

        if curso is None or not curso.ativo:
            return redirect(url_for("cursos"))

        if request.method == "POST":
            curso.nome = request.form["nome"]
            curso.descricao = request.form.get("descricao") or None
            curso.carga_horaria = (
                int(request.form["carga_horaria"])
                if request.form.get("carga_horaria") else None
            )

            db.session.commit()

            return redirect(url_for("cursos"))

        return render_template("editar_curso.html", curso=curso)

    # EXCLUSÃO LÓGICA DE CURSOS
    @app.route("/cursos/excluir/<int:id>", methods=["POST"])
    @login_obrigatorio
    def excluir_curso(id):
        curso = db.session.get(Curso, id)

        if curso is not None:
            curso.ativo = False
            db.session.commit()

        return redirect(url_for("cursos"))

    return app
