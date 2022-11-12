import datetime
import pandas as pd
from models.tables import *

#dfdsf

from config import App
db = App().get_db()
# from models.tables import *

def delete_user(cliente_id:int) -> bool:
    try:

        usuario = Cliente.query.filter_by(cliente_id=cliente_id).first()
        endereco = Endereco_Cliente.query.filter_by(endereco_cliente_id=usuario.endereco_cliente_id).first()
        conta = Conta.query.filter_by(cliente_id=usuario.cliente_id).first()
        # extrato = Extrato.query.filter_by(conta_id=conta.first().conta_id)

        querys_delecao = [
            f"delete from extrato where conta_id = {conta.conta_id}",
            f"delete from conta where cliente_id = {usuario.cliente_id}",
            f"delete from cliente where cliente_id = {usuario.cliente_id}",
            f"delete from endereco_cliente where endereco_cliente_id = {usuario.endereco_cliente_id}",
            f"delete from usuario where cpf = {usuario.cpf}"
        ]

        engine = db.get_engine()
        connection = engine.raw_connection()
        cursor = connection.cursor()
        for query in querys_delecao:
            cursor.execute(query)
            connection.commit()
        cursor.close()

    except Exception as e:
        print(f'Erro ao excluir dados do usuário: {e}')
        return False

    return True

def get_usuarios() -> dict:
    engine =  db.get_engine()

    query = '''
    select 
    c.nome, c.cliente_id, 
    c.data_nascimento, 
    c.sexo ,c.telefone, 
    a.conta, a.saldo, a.tipo 
    from cliente c 
    inner join conta a
    on c.cliente_id = a.cliente_id;
    ''' 
    df = pd.read_sql_query(query, con=engine)
    df = df.to_dict(orient='records')
    return df

def get_movimentacoes():

    data = []
    valor = []

    engine =  db.get_engine()
    df = pd.read_sql_query('select * from extrato', con=engine)

    if df.empty:
        return data, valor

    df = df[['extrato_data', 'valor']]
    df = df.groupby(by='extrato_data', as_index=False, group_keys=True).sum()
    data = df['extrato_data'].to_list() or [datetime.datetime.now().strftime('%d/%m/%Y')]
    valor = df['valor'].to_list() or [0]
    
    return data, valor
    
def get_transacoes():
    engine = db.get_engine()
    query = 'select * from cliente'
    df = pd.read_sql_query(query, con=engine)
    df = df.to_dict()
    return df

