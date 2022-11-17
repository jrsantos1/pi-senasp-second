from flask import session, redirect, url_for, render_template, request, flash, send_from_directory, jsonify
from flask_bcrypt import generate_password_hash

import models.tables
from utils.data.user import *
from models.tables import Usuario, Endereco_Cliente, Categoria, Conta, Cliente
from utils.auth.auth import *
from utils.data.admin import get_usuarios 
from utils.chart.chart_admin import *

aplicativo = App()
app = aplicativo.get_app()
db = models.tables.db


@app.route('/admin/login')
def login_admin():
    if 'admin_logado' in session:
        if not (session['admin_logado'] == None):
            return redirect(url_for('admin_home'))
        
    return render_template('admin/admin_login.html')
    

@app.route('/admin/autenticar', methods=['Post'])
def autenticar_admin():
    usuario: str = request.form['usuario']
    senha: str = request.form['senha']
    
    usuario_adm = Usuario_Admin.query.filter_by(admin_usuario=request.form['usuario']).first()
    
    if usuario_adm:
        senha_check = check_password_hash(usuario_adm.admin_senha, senha)
        if senha_check:
            if 'usuario_logado' in session:
                session['usuario_logado'] = None     
            session['admin_logado'] = usuario
            return redirect(url_for('admin_home'))

    return redirect(url_for('login_admin'))
            
@app.route('/admin')
def admin_home():
    
    logado = verifica_admin_logado()
    if not logado:   
        return redirect(url_for('login_admin'))    

    lista_usuarios = get_usuarios()
    
    #grafico_volume = get_grafico_movimentacoes()
    total_cliente = get_total_cliente()
    total_custodia = get_total_valor_em_custodia()
    total_transacoes = get_total_transacoes()
    transacoes_dia_qtd = get_transacoes_dia_qtd()

    # print(total_custodia.total)

    return render_template('/adm/index_adm.html',
                           usuarios = lista_usuarios,
                           total_cliente=total_cliente,
                           total_transacoes=total_transacoes,
                           total_custodia=total_custodia,
                           transacoes_dia_qtd=transacoes_dia_qtd
                           )

@app.route('/admin/editar/<int:id>')
def admin_editar_usuario(id):
    logado = verifica_admin_logado()
    if not logado:
        return redirect(url_for('login_admin'))

    dados_edicao = get_dados_edicao(id)

    return render_template('cadastro/atualizar_usuario.html', dados_edicao=dados_edicao)

@app.route('/admin/editar/atualizar', methods=['POST', 'GET'])
def atualizar_usuario():
    logado = verifica_admin_logado()
    if not logado:
        return redirect(url_for('login_admin'))

    # pegar entidades

    cpf = request.form['cpf']
    cliente = get_cliente(cpf)
    conta = get_conta(cpf)
    endereco = get_endereco_cliente(cpf)
    usuario = get_usuario(cpf)

    # cliente

    cliente.nome = request.form['nome']
    cliente.telefone = request.form['telefone']
    cliente.sexo = request.form['sexo']

    # endereco

    endereco.cep = request.form['cep']
    endereco.uf = request.form['uf']
    endereco.cidade = request.form['cidade']
    endereco.bairro = request.form['bairro']
    endereco.rua = request.form['rua']
    endereco.numero = request.form['numero']
    endereco.complemento = request.form['complemento']

    # conta
    conta.tipo = request.form['tipo']

    # usuario

    usuario.senha = generate_password_hash(request.form['senha']).decode('utf-8')
    usuario.email = request.form['email']

    valida = True
    pilha_de_erros = []

    try:
        db.session.add(usuario)
    except Exception as e:
        valida = False
        pilha_de_erros.append(e)
    try:
        db.session.add(conta)
    except Exception as e:
        valida = False
        pilha_de_erros.append(e)
    try:
        db.session.add(endereco)
    except Exception as e:
        valida = False
        pilha_de_erros.append(e)
    try:
        db.session.add(cliente)
    except Exception as e:
        valida = False
        pilha_de_erros.append(e)

    tamanho = len(pilha_de_erros)

    if not valida:
        flash(f'erro ao alterar dados do cliente: {pilha_de_erros}')
        return redirect(url_for('admin_home'))
    else:
        flash('Atualização realizada com sucesso')
        return  redirect(url_for('admin_home'))


@app.route('/admin/excluir/<int:id>')
def admin_excluir_usuario(id):
    logado = verifica_admin_logado()
    if not logado:
        return redirect(url_for('login_admin'))

    usuario_id = id

    deletar = delete_user(usuario_id);

    if deletar:
        flash('Operação realizada com sucesso')
        return redirect(url_for('admin_home'))
    return redirect(url_for('admin_clientes'))


# rota para realizar logout
@app.route("/admin/logout")
def logout_admin():
    if 'admin_logado' in session:
        session['admin_logado'] = None
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('admin_home'))

@app.route("/admin/clientes")
def admin_clientes():
    logado = verifica_admin_logado()

    if not logado:
        return redirect(url_for('login_admin'))


    clientes = get_clientes()

    return render_template('adm/clientes.html',
                           clientes=clientes)

@app.route('/admin/ordens')
def transacoes():
    logado = verifica_admin_logado()

    if not logado:
        return redirect(url_for('login_admin'))

    return render_template('adm/ordens.html')

