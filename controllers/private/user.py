
# libs externas
from tempfile import template
import win32com.client as wincl
from jinja2 import FileSystemLoader, Environment

import json
import pythoncom 
import pandas as pd
import email
from models.tables import *
from flask import session, redirect, url_for, render_template, request, flash
import locale

# libs projeto
from utils.chart.chart_user import *
from config import App
from utils.auth.auth import *
from utils.email import config_email as e_mail
from utils.data.user import *

from utils.conta.transferencia import *
from utils.data.cotacoes import get_cotacoes 


aplicativo = App()
app = aplicativo.get_app()

@app.template_filter()
def moeda(value):
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8') 
    format = locale.currency(value)
    return format
    
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
    extrato = get_extrato(cpf, size=5)   
    
    extrato.saldo_atual = lambda x : str(locale.currency(x))
    
    # obter json grafico 
    graphJSON = get_chart_user_historico_movimentacoes(cpf)
    
    # obter cotacoes atuais
    cotacoes = get_cotacoes()
    
    dolar = float(cotacoes['dolar']['today'])
    
    return render_template('user/home.html', cliente = cliente, conta = conta, extrato=extrato,graphJSON=graphJSON, cotacao=cotacoes)

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
    
    # valida = verificarUsuarioLogado()
    #
    # if valida:
    #     print(valida)
    #     return redirect(url_for('login'))
        
    cpf =  request.form['cpf']
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    usuario = Usuario.query.filter_by(cpf=cpf).first()
    
    # recebendo dados de endereço
    
    cep = request.form['cep']
    bairro = request.form['bairro']
    uf = request.form['uf']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
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
        print('cliente existe')
        flash('usuário já existe')
        redirect(url_for('login'))
            
    else:

        # criando novo cliente
        print('criando cliente')

        nome = request.form['nome']
        nascimento = request.form['nascimento']
        telefone = request.form['telefone']
        sexo = request.form['sexo']

        cliente = Cliente(cpf=cpf, nome=nome, data_nascimento=nascimento, telefone=telefone, endereco_cliente_id=endereco.endereco_cliente_id, sexo=sexo)
        db.session.add(cliente)
        db.session.commit()

        # salvando foto
        # arquivo = request.files ['arquivo']
        # image_path = aplicativo.get_path().join('/uploads')
        # arquivo.save(f'{image_path}/{cliente.cliente_id}.jpg')

        # criando novo usuário

        email =  request.form['email']
        senha = request.form['senha']

        usuario = Usuario(email=email, senha=senha, cpf=cpf)
        db.session.add(usuario)
        db.session.commit()

        #criando nova conta

        conta_numero = request.form['conta']
        saldo = 0
        tipo = request.form['tipo']

        conta = Conta(conta=conta_numero, saldo=saldo, tipo=tipo, cliente_id=cliente.cliente_id)
        db.session.add(conta)
        db.session.commit()

        # derrubando sessão
        session['usuario_logado'] = None

        flash('Seu cadastro foi criado com sucesso')
        return redirect(url_for('login'))

    return redirect(url_for('login'))

# Direcionar par tela de transacao
@app.route('/user/transacao')
def transacao():

    valida = verificarUsuarioLogado()

    if valida:
        print(valida)
        return redirect(url_for('login'))

    return redirect(url_for('index_user'))

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