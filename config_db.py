from errno import errorcode
from tkinter import E
import mysql.connector 
from mysql.connector import errorcode


try: 
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root123"
    )
    print("Conexão realizada com sucesso")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Nome de usuário ou senha errados')
    else:
        print(err)
        
        
