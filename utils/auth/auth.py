from flask import session, redirect, url_for, request, flash
from models.tables import *

def verificarUsuarioLogado():
    if ('usuario_logado' not in session or session['usuario_logado'] == None):
        return redirect(url_for('login'))
    else:
        pass
def verifica_admin_logado():
    if ('admin_logado' not in session or session['admin_logado'] == None):
        return False
    else:
        return True

def autenticar_usuario(cpf: str, senha: str):
    
    # verificando se há usuário no banco de dados com consulta
    usuario = Usuario.query.filter_by(cpf=request.form['cpf']).first()
    if usuario:
        if senha == usuario.senha:
            session['usuario_logado'] = usuario.cpf
            cliente = Cliente.query.filter_by(cpf=cpf).first()
            return True
    return False