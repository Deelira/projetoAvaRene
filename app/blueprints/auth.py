from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..services.usuario_service import UsuarioService, login_required
from ..models.usuario import TipoUsuario


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    """Redireciona a raiz para o dashboard."""
    return redirect(url_for("auth.dashboard"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if 'usuario_id' in session:          # já logado? manda pro dashboard
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        usuario = UsuarioService().autenticar(email, senha)
        if usuario:
            session['usuario_id'] = usuario.id      # ← troca login_user()
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("auth.dashboard"))
        flash("E-mail ou senha inválidos.", "danger")
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """GET: exibe o formulário. POST: cria o usuário via service."""
    # ← troca current_user.is_authenticated
    if 'usuario_id' in session:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")

        # Captura o tipo escolhido no formulário
        tipo_form = request.form.get("tipo", "cliente")

        # Converte a string do HTML para o Enum do Python
        if tipo_form == "prestador":
            tipo_enum = TipoUsuario.PRESTADOR
        else:
            tipo_enum = TipoUsuario.CLIENTE

        try:
            UsuarioService().criar_usuario(nome, email, senha, tipo_enum)
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as erro:
            flash(str(erro), "danger")

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    session.pop('usuario_id', None)                 # ← troca logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/tornar-prestador", methods=["POST"])
@login_required
def tornar_prestador():
    """Rota acionada quando o cliente clica no botão 'Quero ser Prestador'."""
    try:
        # ← troca current_user.id por session['usuario_id']
        UsuarioService().tornar_prestador(session['usuario_id'])
        flash("Parabéns! Sua conta foi atualizada. Agora você também pode oferecer serviços.", "success")
    except ValueError as erro:
        flash(str(erro), "danger")

    return redirect(url_for("auth.dashboard"))


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    """Página protegida — só aparece para usuário logado."""
    # ← troca current_user por usuario_logado()
    usuario = UsuarioService().usuario_logado()
    return render_template("dashboard.html", usuario=usuario)