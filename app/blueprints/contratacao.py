from flask import Blueprint, render_template, redirect, url_for, flash, session

from ..services.contratacao_service import ContratacaoService
from ..services.usuario_service import UsuarioService, login_required
from ..models.usuario import TipoUsuario

contratacao_bp = Blueprint("contratacao", __name__, url_prefix="/contratacoes")


@contratacao_bp.route("/nova/<int:servico_id>", methods=["POST"])
@login_required
def nova(servico_id):
    """Rota acionada quando o cliente clica em 'Contratar' no catálogo."""
    usuario = UsuarioService().usuario_logado()     # ← troca current_user
    try:
        # Passamos o usuario inteiro para o service validar o tipo
        ContratacaoService().contratar_servico(usuario, servico_id)
        flash("Serviço contratado com sucesso! O prestador entrará em contato.", "success")
    except ValueError as erro:
        flash(str(erro), "danger")

    # Após contratar, volta para o catálogo
    return redirect(url_for("servico.catalogo"))


@contratacao_bp.route("/minhas")
@login_required
def minhas():
    """Lista as contratações feitas pelo usuário logado (seja cliente ou prestador)."""
    usuario = UsuarioService().usuario_logado()
    # REMOVIDO O BLOQUEIO PARA PERMITIR PRESTADORES AQUI
    contratacoes = ContratacaoService().listar_minhas_contratacoes(usuario.id)
    return render_template("contratacao_listar.html", contratacoes=contratacoes, is_cliente=True)


@contratacao_bp.route("/recebidas")
@login_required
def recebidas():
    """Lista os pedidos que o prestador logado recebeu."""
    usuario = UsuarioService().usuario_logado()

    if usuario.tipo != TipoUsuario.PRESTADOR:
        flash("Acesso restrito a prestadores.", "warning")
        return redirect(url_for("auth.dashboard"))

    contratacoes = ContratacaoService().listar_pedidos_recebidos(usuario.id)
    return render_template("contratacao_listar.html", contratacoes=contratacoes, is_cliente=False)