import datetime

from click._termui_impl import Editor
from flask import flash, request, redirect, url_for, session
from utils.conta.helpers import verificar_saldo
from utils.data.user import *
from utils.email import config_email as e_mail

def gerar_transferencia(cpf_destinatario: str, tipo: str, categoria: str):

    valor = request.form['valor']
    conta = get_conta(cpf_destinatario)
    usuario = get_usuario(cpf_destinatario)
    cliente_logado = Cliente.query.filter_by(cpf=session['usuario_logado']).first()
    conta_logado = Conta.query.filter_by(cliente_id=cliente_logado.cliente_id).first()

    # validacoes

    if not(conta) or conta == None: 
        flash('Conta de destino não existe')
        #return redirect(url_for('transacao'))
        return False
    
    if conta_logado.saldo < float(valor):
         flash('saldo insuficiente')
         return False
         #return redirect(url_for('transacao'))

    if conta_logado.conta_id == conta.conta_id:
        flash('Erro 23423. Não é possível realizar transferência para a conta de origem')
        return False
    
    data = request.form['data']
    data = datetime.datetime.now().strftime('%Y-%m-%d')
    # salvando transacao

    operacao = Operacao.query.filter_by(operacao_tipo=tipo).first()
    categoria_ = Categoria.query.filter_by(categoria_descricao=categoria).first()

    try:

        transacao = Transacao(
            conta_origem_id=conta_logado.conta_id, 
            conta_destino_id=conta.conta_id, 
            transacao_data=data, 
            valor=valor, 
            operacao_id=operacao.operacao_id,
            categoria_id=categoria_.categoria_id
        )
        
        db.session.add(transacao)
        db.session.commit()
        
        # alterando saldos 
        
        novo_valor = float(valor)
        conta_logado.saldo -= novo_valor
        conta.saldo += novo_valor
        db.session.add(conta_logado)
        db.session.add(conta)
        db.session.commit()
        
        # gerando extrato
        saldo_extrado_saida = novo_valor - (novo_valor * 2) 
        extrato_saida = Extrato(
            conta_id=conta_logado.conta_id,
            extrato_data=data, fluxo='Saída',
            valor=saldo_extrado_saida,
            saldo_atual=conta_logado.saldo,
            operacao=tipo,
            categoria=categoria_.categoria_descricao)

        extrato_entrada = Extrato(
            conta_id=conta.conta_id,
            extrato_data=data,
            fluxo='Entrada',
            valor=valor,
            saldo_atual=conta.saldo,
            operacao=tipo,
            categoria=categoria_.categoria_descricao)
            
        db.session.add(extrato_saida)
        db.session.add(extrato_entrada)
        
        db.session.commit()
    except Exception as e:
        print(f"Ocorreu um erro durante a realização da transferêcia {e}")
        flash('Erro ao registrar transacao')
        return False

    #enviar e-mail
    
    try:
        dados_email = {
            'valor': valor,
            'destinatario':conta,
            'data': data
        }
        
        template = e_mail.carregar_template(dados_email, 'email/email_transferencia_realizada.html')
        e_mail.enviar(destinatario=conta_logado.email, template=template)
        
        dados_email = {
            'nome' : 'teste',
            'valor': valor,
            'remetente':cliente_logado.cpf,
            'data': data
        }
        
        template_transferencia_recebida = e_mail.carregar_template(dados_email,'email/email_transferencia_recebida.html' )
        e_mail.enviar(destinatario=usuario.email, template=template_transferencia_recebida)
    except Exception as e:
        print(f"Erro ao realizar envio de e-mail {e}")
    
    flash("Transferência realizada com sucesso")
    return True

def sacar(valor, categoria):
    conta: Conta = get_conta(session['usuario_logado'])
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    valor = float(valor)
    tem_saldo = verificar_saldo(valor=valor, conta=conta)

    if tem_saldo:
        flash('Saldo insuficiente')
        return False


    try:
        conta.saldo -= valor
        db.session.add(conta)

    except: 
        print("Erro ao atualizar saldo")

    categoria_ = Categoria.query.filter_by(categoria_descricao=categoria).first()

    transacao = Transacao(
        conta_origem_id=conta.conta_id, 
        conta_destino_id=conta.conta_id, 
        transacao_data=data, 
        valor=valor, 
        operacao_id=4,
        categoria_id=categoria_.categoria_id
        )

    try:
        db.session.add(transacao)
    except: 
        print("Erro ao gerar nova transação")

    valor_saida = valor * (-1)

    try:
        operacao = Operacao.query.filter_by(operacao_id=transacao.operacao_id).first()
        extrato = Extrato(
            conta_id=conta.conta_id,
            extrato_data=data,
            fluxo='Saída',
            valor=valor_saida,
            saldo_atual=conta.saldo,
            operacao=operacao.operacao_tipo,
            categoria=categoria_.categoria_descricao)
        db.session.add(extrato)
    except: 
        print("Erro ao gerar nova transação")

    
    try:
        db.session.commit()
    except:
        print("Erro ao concluir operação")

    return True

    
def depositar(valor, categoria):
    conta: Conta = get_conta(session['usuario_logado'])
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    valor = float(valor)

    if valor > 10000:
        flash('Não é possível transferir valores acima de 10 mil reais em uma única operação')
        return False

    if valor < 0.5:
        flash('Não é possível transferir valores abaixo de R$ 0,50 (50 Centavos)')
        return False

    try:

        conta.saldo += valor
        db.session.add(conta)
        db.session.commit()

        categoria_ = Categoria.query.filter_by(categoria_descricao=categoria).first()

        transacao = Transacao(
            conta_origem_id=conta.conta_id,
            conta_destino_id=conta.conta_id,
            transacao_data=data,
            valor=valor,
            operacao_id=5,
            categoria_id=categoria_.categoria_id)
        db.session.add(transacao)
        db.session.commit()

        operacao = Operacao.query.filter_by(operacao_id=transacao.operacao_id).first()

        extrato = Extrato(
            conta_id=conta.conta_id,
            extrato_data=data,
            fluxo='Entrada',
            valor=valor,
            saldo_atual=conta.saldo,
            operacao=operacao.operacao_tipo,
            categoria=categoria_.categoria_descricao)

        db.session.add(extrato)
        db.session.commit()
        
    except Exception as e:
        print("Erro ao gerar nova transação" + e.with_traceback())

    return True