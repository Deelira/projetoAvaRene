from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from ..services.contratacao_service import ContratacaoService
from ..models.usuario import TipoUsuario

contratacao_bp = Blueprint("contratacao", __name__, url_prefix="/contratacoes")


@contratacao_bp.route("/nova/<int:servico_id>", methods=["POST"])
@login_required
def nova(servico_id):
    """Rota acionada quando o cliente clica em 'Contratar' no catálogo."""
    try:
        # Passamos o current_user inteiro para o service validar o tipo
        ContratacaoService().contratar_servico(current_user, servico_id)
        flash("Serviço contratado com sucesso! O prestador entrará em contato.", "success")
    except ValueError as erro:
        flash(str(erro), "danger")
    
    # Após contratar, volta para o catálogo
    return redirect(url_for("servico.catalogo"))


@contratacao_bp.route("/minhas")
@login_required
def minhas():
    """Lista as contratações feitas pelo usuário logado (seja cliente ou prestador)."""
    # REMOVIDO O BLOQUEIO PARA PERMITIR PRESTADORES AQUI
    contratacoes = ContratacaoService().listar_minhas_contratacoes(current_user.id)
    return render_template("contratacao_listar.html", contratacoes=contratacoes, is_cliente=True)


@contratacao_bp.route("/recebidas")
@login_required
def recebidas():
    """Lista os pedidos que o prestador logado recebeu."""
    if current_user.tipo != TipoUsuario.PRESTADOR:
        flash("Acesso restrito a prestadores.", "warning")
        return redirect(url_for("auth.dashboard"))

    contratacoes = ContratacaoService().listar_pedidos_recebidos(current_user.id)
    return render_template("contratacao_listar.html", contratacoes=contratacoes, is_cliente=False)