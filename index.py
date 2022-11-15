import string
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Date
from config import App
from models.tables import *
from controllers.private import user, admin  
from controllers.public import routes
from flask_bcrypt import Bcrypt

#configuracao

aplicativo = App()
app = aplicativo.get_app()
app.app_context().push()
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)