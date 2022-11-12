import datetime
from flask import flash, request, redirect, url_for, session
from utils.conta.helpers import verificar_saldo
from utils.data.user import *
from utils.email import config_email as e_mail

def gerar_transferencia(cpf_destinatario):
    conta_destino = get_conta(cpf_destinatario)
    valor = request.form['valor']
    conta = get_conta(cpf_destinatario)
    cliente_logado = Cliente.query.filter_by(cpf=session['usuario_logado']).first()
    conta_logado = Conta.query.filter_by(cliente_id=cliente_logado.cliente_id).first()
    user_cliente_logado = Usuario.query.filter_by(cpf=cliente_logado.cpf).first()
    cliente_destinatario = Cliente.query.filter_by(cliente_id=conta.cliente_id).first()
    user_cliente_destinatario = Usuario.query.filter_by(cpf=cliente_destinatario.cpf).first() 
    
    # validacoes

    if not(conta) or conta == None: 
        flash('Conta de destino não existe')
        #return redirect(url_for('transacao'))
        return False
    
    if conta_logado.saldo < float(valor):
         flash('saldo insuficiente')
         return False
         #return redirect(url_for('transacao'))
    
    data = request.form['data']
    data = datetime.datetime.now().strftime('%Y-%m-%d')
    tipo = request.form['tipo']
    
    # salvando transacao
    
    try:
    
        transacao = Transacao(
            conta_origem_id=conta_logado.conta_id, 
            conta_destino_id=conta.conta_id, 
            transacao_data=data, 
            valor=valor, 
            operacao_id=tipo)
        
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
        extrato_saida = Extrato(conta_id=conta_logado.conta_id, extrato_data=data, fluxo='Saída', valor=saldo_extrado_saida, saldo_atual=conta_logado.saldo)
        extrato_entrada = Extrato(conta_id=conta.conta_id, extrato_data=data, fluxo='Entrada', valor=valor, saldo_atual=conta.saldo)
            
        db.session.add(extrato_saida)
        db.session.add(extrato_entrada)
        
        db.session.commit()
    except:
        
        print("Ocorreu um erro durante a realização da transferêcia")
    
    # enviar e-mail 
    
    # try:
    
    #     dados_email = {
    #         'valor': valor,
    #         'destinatario':conta_destino,
    #         'data': data
    #     }
        
    #     template = e_mail.carregar_template(dados_email, 'email/email_transferencia_realizada.html')
    #     e_mail.enviar(destinatario=user_cliente_logado.email, template=template)
        
    #     dados_email = {
    #         'nome' : 'teste',
    #         'valor': valor,
    #         'remetente':user_cliente_logado.cpf,
    #         'data': data
    #     }
        
    #     template_transferencia_recebida = e_mail.carregar_template(dados_email,'email/email_transferencia_recebida.html' )
    #     e_mail.enviar(destinatario=user_cliente_destinatario.email, template=template_transferencia_recebida)
    # except:
    #     print("Erro ao realizar envio de e-mail")
    
    flash("Transferência realizada com sucesso")
    return True

def sacar(valor):
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

    transacao = Transacao(
        conta_origem_id=conta.conta_id, 
        conta_destino_id=conta.conta_id, 
        transacao_data=data, 
        valor=valor, 
        operacao_id=4)

    try:
        db.session.add(transacao)

    except: 
        print("Erro ao gerar nova transação")

    valor_saida = valor * (-1)
    
    

    try:
        extrato = Extrato(conta_id=conta.conta_id, extrato_data=data, fluxo='Saída', valor=valor_saida, saldo_atual=conta.saldo)
        db.session.add(extrato)
    except: 
        print("Erro ao gerar nova transação")

    
    try:
        db.session.commit()
    except:
        print("Erro ao concluir operação")
    
    flash("Operação realizada com sucesso")
    return True

    
def depositar(valor):
    conta: Conta = get_conta(session['usuario_logado'])
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    valor = float(valor)

    if valor < 0:
        flash('Valor não pode ser menor que 0')
        return False

    try:

        conta.saldo += valor
        db.session.add(conta)
        db.session.commit()


        transacao = Transacao(
            conta_origem_id=conta.conta_id,
            conta_destino_id=conta.conta_id,
            transacao_data=data,
            valor=valor,
            operacao_id=4)
        db.session.add(transacao)
        db.session.commit()

        extrato = Extrato(conta_id=conta.conta_id, extrato_data=data, fluxo='Entrada', valor=valor, saldo_atual=conta.saldo)
        db.session.add(extrato)
        db.session.commit()
        
    except Exception as e:
        print("Erro ao gerar nova transação" + e.with_traceback())


    flash("Operação realizada com sucesso")
    return True