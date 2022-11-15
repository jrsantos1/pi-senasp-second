import os
import random

from models.tables import Conta

def verificar_saldo(valor: float, conta: Conta):
    if valor < conta.saldo:
        return False
    else:
        return True

def formt_conta(cliente_id):
    conta_formatada = f'{str(cliente_id).zfill(9)}-{random.randint(1,5)}'
    return conta_formatada

def format_cpf(cpf: str):
    cpf_formatado = cpf.replace('-','').replace('.','')
    return cpf_formatado

def recupera_imagem(conta):
    for item in os.listdir('../../uploads'):
        if f'{conta}.jpg' == item:
            return str(conta)
        else:
            return 'capa_padrao'
    