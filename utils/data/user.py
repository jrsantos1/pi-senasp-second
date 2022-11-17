from cgitb import text
from flask import session
from models.tables import *
from sqlalchemy import asc, desc
import pandas as pd

def get_cliente(cpf)-> Cliente : 
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    return cliente

def get_conta(cpf) -> Conta:
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    conta = Conta.query.filter_by(cliente_id=cliente.cliente_id).first()
    return conta

def get_extrato(cpf, size) -> Extrato:
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    conta = Conta.query.filter_by(cliente_id=cliente.cliente_id).first()
    extrato = Extrato.query.filter_by(conta_id=conta.conta_id).order_by(desc('extrato_data')).limit(size)
    return extrato
def get_endereco_cliente(cpf) -> Endereco_Cliente :
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    endereco = Endereco_Cliente.query.filter_by(endereco_cliente_id=cliente.endereco_cliente_id).first()
    return endereco

def get_usuario(cpf) -> Usuario:
    usuario = Usuario.query.filter_by(cpf=cpf).first()
    return usuario

def get_percentual_transacoes(conta_id):
    engine = db.get_engine()
    query = f'''  select  operacao, sum(abs(valor)) as 'total' from extrato 
            where 
            conta_id = {conta_id}
            and DATE_FORMAT(extrato_data, "%Y") >= DATE_FORMAT(curdate(), "%Y")
            group by operacao; '''
    df = pd.read_sql_query(query, con=engine)
    df = df.to_dict(orient='records')

    valor_nominal = {}
    total = 0
    for item in df:
        total += item['total']
        valor_nominal[item['operacao']] = item['total']

    valor_percentual = {}

    for item in df:
        valor_percentual[item['operacao']] = round(item['total'] / total * 100, 2)

    return valor_nominal, valor_percentual

def get_contatos(conta_id:int):
    engine = db.get_engine()
    
    
    
    query = f''' 
    select distinct
     cli.nome
    ,cli.telefone
    ,u.email 
    ,cli.cpf
    ,c.conta
     from 
    (select * from transacao where conta_origem_id = {conta_id} or conta_destino_id = {conta_id}) 
    tabela_nova 
    inner join conta c
    on (c.conta_id = tabela_nova.conta_origem_id or c.conta_id = tabela_nova.conta_destino_id) and c.conta_id != {conta_id}
    inner join cliente cli
    on cli.cliente_id = c.cliente_id
    inner join usuario u
    on u.cpf = cli.cpf
    where tabela_nova.conta_origem_id != {conta_id} or tabela_nova.conta_destino_id != {conta_id}
    '''

    df = pd.read_sql_query(query, con=engine)
    df = df.to_dict(orient='records')

    return df

