import string
import win32com.client as wincl
from jinja2 import FileSystemLoader, Environment
import pythoncom 

def carregar_template(dados, path_template):
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader)
    template = env.get_template(path_template)
    file = open('templates/email/outputs/index.html', 'w')
    render = template.render(dados_user = dados)
    file.write(render)
    file.close()
    
    print("template carregado")
    return render

def enviar(destinatario: string, template):
     
    pythoncom.CoInitialize()
    print("outlook inicializado")
    outlook = wincl.Dispatch('outlook.application')
    print("outlook carregado")
    # criando e-mail a partir da ingregracao com outlook
    email = outlook.CreateItem(0) 
    print("email criado") 
    # configurando informacoes do email
    # Para quem vai o e-mail // Assunto da mensagem
    email.To = destinatario 
    # email.Cc = "jhonatan.loko25@gmail.com"
    email.Subject = 'Banco JM²'
    # Criando e adicionando anexo
    # anexo = "C:\Git-Projects\\automates\\teste envio de email\email.xlsx"
    # email.Attachments.Add(anexo)
    email.HTMLBody = template
    email.Display()

    
   
#enviar("jhonatanjonh@outlook.com", template=carregar_template())
