from cgitb import text
from flask import session
from models.tables import *
from sqlalchemy import asc, desc

def get_cliente(cpf)-> Cliente : 
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    return cliente

def get_conta(cpf) -> Conta:
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    print(cliente)
    print(cliente.cliente_id)
    conta = Conta.query.filter_by(cliente_id=cliente.cliente_id).first()
    print(conta)
    return conta

def get_extrato(cpf, size) -> Extrato :
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    conta = Conta.query.filter_by(cliente_id=cliente.cliente_id).first()
    extrato = Extrato.query.filter_by(conta_id=conta.conta_id).order_by(desc('extrato_data')).limit(size)
    return extrato

