from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ..services.servico_service import ServicoService
from ..models.usuario import TipoUsuario

# Criamos o Blueprint com o prefixo /servicos
servico_bp = Blueprint("servico", __name__, url_prefix="/servicos")


@servico_bp.route("/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    """Apenas PRESTADORES podem cadastrar serviços."""

    # 1. Controle de Acesso: Barrando clientes
    if current_user.tipo != TipoUsuario.PRESTADOR:
        flash("Acesso negado. Apenas prestadores podem cadastrar serviços.", "warning")
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        descricao = request.form.get("descricao", "")
        preco = request.form.get("preco", "")

        try:
            # O Service vai validar e salvar no banco.
            # Passamos current_user.id para amarrar o serviço ao prestador logado.
            ServicoService().criar_servico(current_user.id, titulo, descricao, preco)
            flash("Serviço cadastrado com sucesso!", "success")
            return redirect(url_for("servico.meus_servicos"))
        except ValueError as erro:
            flash(str(erro), "danger")

    return render_template("servico_cadastrar.html")


@servico_bp.route("/meus-servicos")
@login_required
def meus_servicos():
    """Lista os serviços criados pelo prestador logado."""
    if current_user.tipo != TipoUsuario.PRESTADOR:
        flash("Acesso negado. Área restrita para prestadores.", "warning")
        return redirect(url_for("auth.dashboard"))

    servicos = ServicoService().listar_servicos_do_prestador(current_user.id)
    return render_template("servico_listar.html", servicos=servicos, is_meus_servicos=True)


@servico_bp.route("/catalogo")
@login_required
def catalogo():
    """Lista todos os serviços para os clientes verem e contratarem."""
    servicos = ServicoService().listar_catalogo()
    return render_template("servico_listar.html", servicos=servicos, is_meus_servicos=False)