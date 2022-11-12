from ntpath import join
import os
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Date

#configuracao
class App:
    app = Flask(__name__)
    app.secret_key = 'BANCO_MJ'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
            SGBD = 'mysql+mysqlconnector',
            usuario = 'root',
            senha = 'root123',
            servidor = 'localhost',
            database = 'jm_banco')
                
    def get_app(self):
        return self.app
    
    def get_db(self):
        db = SQLAlchemy(self.app)
        return db
    
    def get_engine_db(self):
        return self.get_db()
    
    def get_path(self):
        return os.path.dirname(os.path.abspath(__file__))