from models.tables import *
import string
from flask import session, redirect, url_for, render_template, request, flash, send_from_directory
from config import App
import plotly
import plotly.express as px
import json
import pandas as pd
from utils.auth.auth import *

aplicativo = App()
app = aplicativo.get_app()

# Página inicial
@app.route("/")
def home():
    return render_template("home.html", titulo="Lista")

@app.route("/sobre", methods=['GET', 'POST'])
def sobre():
    return render_template("sobre.html", titulo="sobre")

@app.route("/abrir_conta")
def abrir_conta():
    return render_template("user/abrir_conta.html", titulo="criar template")

@app.route("/login")
def login():
    if 'usuario_logado' in session:
        if not (session['usuario_logado'] == None):
            return redirect(url_for('index_user'))
        
    return render_template("user/login.html", titulo="login")

@app.route('/adicionar_foto/<nome_arquivo>')
def adicionar_foto(nome_arquivo):
     return send_from_directory('uploads', nome_arquivo)