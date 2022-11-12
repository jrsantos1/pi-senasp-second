from models.tables import Conta

def verificar_saldo(valor: float, conta: Conta):
    if valor < conta.saldo:
        return False
    else:
        return True
    