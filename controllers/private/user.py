
# libs externas
from tempfile import template
import win32com.client as wincl
from jinja2 import FileSystemLoader, Environment

import json
import pythoncom 
import pandas as pd
import email
from models.tables import *
from flask import session, redirect, url_for, render_template, request, flash, send_from_directory
from flask_bcrypt import generate_password_hash
import locale

# libs projeto
from utils.chart.chart_user import *
from config import App
from utils.auth.auth import *
from utils.conta.helpers import formt_conta, format_cpf
from utils.email import config_email as e_mail
from utils.data.user import *

from utils.conta.transferencia import *
from utils.data.cotacoes import get_cotacoes 
import os

aplicativo = App()
app = aplicativo.get_app()

@app.template_filter()
def moeda(value):
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8') 
    format = locale.currency(value)
    return format

@app.template_filter()
def percentual(value):
    value = int(value)
    return 0
    
# rota inicial usuário
@app.route("/user")
def index_user():
   
    valida = verificarUsuarioLogado()
    if valida:
        print(valida)
        return redirect(url_for('login'))
    
    cpf = session['usuario_logado']
    cliente = get_cliente(cpf)
    conta = get_conta(cpf)
    extrato = get_extrato(cpf, size=6)

    extrato.saldo_atual = lambda x : str(locale.currency(x))
    
    # obter json grafico

    grafico_js = get_grafico_movimentacoes(cpf)

    # obter cotacoes atuais
    cotacoes = get_cotacoes()
    
    dolar = float(cotacoes['dolar']['today'])

    valor_nominal, valor_percentual = get_percentual_transacoes(conta.conta_id)
    # caminho pasta list dir
    image_path = os.listdir('C:\code\projetos\python\senac\pi-senac-final\\uploads')

    #return render_template('user_/home.html', cliente = cliente, conta = conta, extrato=extrato,graphJSON=graphJSON, cotacao=cotacoes)
    return render_template('user/index_user.html',
                           cliente=cliente,
                           conta=conta,
                           extrato=extrato,
                           cotacao=cotacoes,
                           valor_percentual=valor_percentual,
                           image_path = image_path)

@app.route('/user/contatos')
def contatos():

    valida = verificarUsuarioLogado()
    if valida:
        print(valida)
        return redirect(url_for('login'))

    cpf = session['usuario_logado']
    cliente = get_cliente(cpf)
    conta = get_conta(cpf)

    contatos = get_contatos(conta.conta_id);
    image_path = os.listdir('C:\code\projetos\python\senac\pi-senac-final\\uploads')

    return render_template('user/contatos.html',
                           conta=conta,
                           cliente=cliente,
                           contatos=contatos,
                           image_path=image_path)

@app.route('/user/relatorio')
def relatorio():
    valida = verificarUsuarioLogado()
    if valida:
        print(valida)
        return redirect(url_for('login'))

    cpf = session['usuario_logado']
    cliente = get_cliente(cpf)
    conta = get_conta(cpf)

    grafico_js = get_grafico_movimentacoes(cpf)
    grafico_despesas = get_grafico_despesas(cpf)
    grafico_movimentacoes_user = get_grafico_movimentacoes_por_usuario(conta.conta_id)


    grafico = {
        'movimentacoes' : grafico_js,
        'despesas' : grafico_despesas
    }
    image_path = os.listdir('C:\code\projetos\python\senac\pi-senac-final\\uploads')
    return render_template('./user/analytics_user.html',
                           conta=conta,
                           cliente=cliente,
                           grafico_js=grafico_js,
                           grafico_despesas=grafico_despesas,
                           grafico_movimentacoes_user=grafico_movimentacoes_user,
                           image_path=image_path
                           )


@app.route('/user/extrato', methods=['GET'])
def extrato():

    valida = verificarUsuarioLogado()
    if valida:
        print(valida)
        return redirect(url_for('login'))

    cpf = session['usuario_logado']
    conta = get_conta(cpf)
    cliente = get_cliente(cpf)
    extrato = get_extrato(cpf, size=100)

    image_path = os.listdir('C:\code\projetos\python\senac\pi-senac-final\\uploads')
    return render_template("user/extrato.html",
                           conta=conta,
                           cliente=cliente,
                           extrato=extrato,
                           image_path=image_path)

# rota para realizar logout
@app.route("/user/logout")
def logout():
    if 'usuario_logado' in session:
        session['usuario_logado'] = None
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

# rota para criar novo usuário
@app.route("/novo_usuario", methods=['POST'])
def novo_usuario():

    cpf = format_cpf(request.form['cpf'])
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    usuario = Usuario.query.filter_by(cpf=cpf).first()
    
    # recebendo dados de endereço
    
    cep = request.form['cep']
    uf = request.form['uf']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    rua = request.form['rua']
    numero = request.form['numero']
    complemento = request.form['complemento']
    
    endereco = Endereco_Cliente(
        cep=cep,
        uf = uf,
        cidade = cidade,
        bairro = bairro,
        rua = rua,
        numero = numero,
        complemento = complemento)
    
    try:
        db.session.add(endereco)
        db.session.commit()
    except:
        print("ocorreu um erro durante o cadastro do endereço")
    
    if cliente or usuario:
        flash('Usuário já existe')
        redirect(url_for('login'))


    # criando novo cliente
    print('criando cliente')

    nome = request.form['nome']
    nascimento = datetime.datetime.strptime(request.form['nascimento'], '%d/%m/%Y')
    telefone = request.form['telefone']
    sexo = request.form['sexo']

    cliente = Cliente(cpf=cpf, nome=nome, data_nascimento=nascimento, telefone=telefone, endereco_cliente_id=endereco.endereco_cliente_id, sexo=sexo)
    db.session.add(cliente)
    db.session.commit()

    # criando novo usuário

    email =  request.form['email']
    senha =  generate_password_hash(request.form['senha']).decode('utf-8')

    usuario = Usuario(email=email, senha=senha, cpf=cpf)
    db.session.add(usuario)
    db.session.commit()

    #criando nova conta

    conta_numero = formt_conta(cliente.cliente_id)
    saldo = 0
    tipo = request.form['tipo']

    conta = Conta(conta=conta_numero, saldo=saldo, tipo=tipo, cliente_id=cliente.cliente_id)
    db.session.add(conta)
    db.session.commit()

    conta_id_ = conta.conta


    # salvando foto

    arquivo = request.files['arquivo'] or None
    if arquivo:
        image_path = 'C:\code\projetos\python\senac\pi-senac-final\\uploads'
        # to do image_path = aplicativo.get_path().join('/uploads')
        arquivo.save(f'{image_path}/{conta.conta}.jpg')

    # derrubando sessão
    session['usuario_logado'] = None

    flash('Seu cadastro foi criado com sucesso')
    return redirect(url_for('login'))

# rota para realizar transferência
@app.route("/user/transferir", methods=['POST'])
def transferir():   
    valida = verificarUsuarioLogado()

    if valida:
        print(valida)
        return redirect(url_for('login'))

   # dados destinatario
    cpf_destinatario = request.form['cpf_destinatario']

    transferencia = gerar_transferencia(cpf_destinatario)

    if transferencia:
        return redirect(url_for('index_user'))
    else:
        return redirect(url_for('transacao'))

@app.route('/user/modal/transferencia')
def modal_transferencia():
    return render_template('user/modal_transacoes.html')


@app.route('/user/transferencia', methods=['POST'])
def transferencia():
    valida = verificarUsuarioLogado()

    if valida:
        print(valida)
        return redirect(url_for('login'))

    # verificar transferencia

    tipo = request.form['tipo_transacao']
    categoria = request.form['categoria']

    if tipo == 'saque':
        valor = request.form['valor']
        saque = sacar(valor=valor, categoria=categoria)

        if saque:
            flash('Saque realizado com sucesso')
            return redirect(url_for('index_user'))
            #return redirect(url_for('teste'))
        else:
            flash('Erro ao realizar saque')
            return redirect(url_for('index_user'))

    elif tipo == 'deposito':
        valor = request.form['valor']
        deposito = depositar(valor, categoria)

        if deposito:
            flash('Depósito realizado com sucesso')
            return redirect(url_for('index_user'))
        else:
            flash('Falha ao realizar deposito')
            return redirect(url_for('index_user'))

    elif tipo in ['pix', 'ted', 'doc']:

        cpf_destinatario = request.form['cpf_destinatario']

        transferencia = gerar_transferencia(cpf_destinatario=cpf_destinatario, tipo=tipo, categoria=categoria)

        if transferencia:
            return redirect(url_for('index_user'))
        else:
            return redirect(url_for('transacao'))

# rota para realizar saque
@app.route("/conta/saque", methods=['POST'])
def saque():
    
    valida = verificarUsuarioLogado()
    
    if valida:
        print(valida)
        return redirect(url_for('login'))
    
    valor = request.form['valor']
    saque = sacar(valor=valor)
    
    if saque: 
        return redirect(url_for('index_user'))
    else: 
        return redirect(url_for('transacao'))

@app.route("/conta/deposito", methods=['POST'])
def deposito():
    valida = verificarUsuarioLogado()
    
    if valida:
        print(valida)
        return redirect(url_for('login'))
    
    valor = request.form['valor']
    
    deposito = depositar(valor)
    
    if deposito:
         return redirect(url_for('index_user'))
    else: 
        return redirect(url_for('transacao'))
        
@app.route("/user/conta", methods=['GET'])
def conta_usuario():
    valida = verificarUsuarioLogado()
    
    if valida:
        print(valida)
        return redirect(url_for('login'))
    
    cpf = session['usuario_logado']
    cliente = get_cliente(cpf)
    conta = get_conta(cpf)
    extrato = get_extrato(cpf, size=5)
    return render_template('user/conta.html', cliente = cliente, conta = conta, extrato=extrato)

# rotas de autenticação
    
@app.route("/autenticar", methods=['POST'])
def autenticar():
    
    cpf: str = request.form['cpf']
    senha: str = request.form['senha']
    
    autentica: bool = autenticar_usuario(cpf, senha)
    
    if autentica:
        return redirect(url_for('index_user'))
    else: 
        flash('falha no login')
        return redirect(url_for('login'))

@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)