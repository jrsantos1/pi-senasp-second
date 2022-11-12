from flask import session, redirect, url_for, render_template, request, flash, send_from_directory
from models.tables import *
aplicativo = App()
from utils.auth.auth import *
app = aplicativo.get_app()
from utils.data.admin import get_usuarios 
from utils.chart.chart_admin import *


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
        if senha == usuario_adm.admin_senha:
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
    
    grafico_volume = get_grafico_movimentacoes()

    return render_template('/admin/admin_home.html', usuarios = lista_usuarios, grafico_volume_movimentacoes = grafico_volume)

@app.route('/admin/editar/<int:id>')
def admin_editar_usuario(id):
    pass

@app.route('/admin/excluir', methods=['POST'])
def admin_excluir_usuario():

    usuario_id = request.form['id']

    deletar = delete_user(usuario_id);

    if deletar:
        flash('Operação realizada com sucesso')
        return redirect(url_for('admin_home'))
    return redirect(url_for('admin_home'))


# rota para realizar logout
@app.route("/admin/logout")
def logout_admin():
    if 'admin_logado' in session:
        session['admin_logado'] = None
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('admin_home'))