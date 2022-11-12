from config import App
db = App().get_db()


class Cliente(db.Model):
    __tablename__ = "cliente"
    cliente_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(20), nullable=False)
    sexo = db.Column(db.String(20))
    nome = db.Column(db.String(50), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(40))
    endereco_cliente_id = db.Column(db.Integer, nullable=False)
    # def __repr__(self) -> str:
    #      return '<Name %r>' % self.name

class Usuario(db.Model):
    __tablename__ = "usuario"
    email = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(50), nullable=False, primary_key=True)
    senha = db.Column(db.String(50), nullable=False)    
    # def __repr__(self) -> str:
    #      return '<Name %r>' % self.name

class Conta(db.Model):
    __tablename__ = "conta"
    conta_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conta = db.Column(db.String(20), nullable=False)
    saldo = db.Column(db.Numeric)
    tipo = db.Column(db.String(20), nullable=False)
    cliente_id = db.Column(db.Integer, nullable=False)
    # def __repr__(self) -> str:
    #      return '<Name %r>' % self.name

class Operacao(db.Model):
    __tablename__ = "operacao"
    operacao_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operacao_tipo = db.Column(db.String(20), nullable=False)
    operacao_statis = db.Column(db.Boolean,nullable=False)

class Transacao(db.Model):
    __tablename__ = "transacao"
    transacao_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conta_origem_id = db.Column(db.Integer, nullable=False)
    conta_destino_id = db.Column(db.Integer, nullable=False)
    transacao_data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Numeric)
    operacao_id = db.Column(db.Integer, nullable=False)

class Extrato(db.Model):
    __tablename__ = "extrato"
    extrato_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conta_id = db.Column(db.Integer, nullable=False)
    extrato_data = db.Column(db.Date, nullable=False)
    fluxo = db.Column(db.String(10), nullable=False)
    valor = db.Column(db.Numeric)
    saldo_atual = db.Column(db.Numeric)

class Endereco_Cliente(db.Model):
    __tablename__ = "endereco_cliente"
    endereco_cliente_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cep = db.Column(db.String(20), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    bairro = db.Column(db.String(20), nullable=False)
    rua = db.Column(db.String(20), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    complemento = db.Column(db.String(50), nullable=True)
    
class Usuario_Admin(db.Model):
    __tablename__ = "usuario_admin"    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_usuario = db.Column(db.String(50), nullable=False)
    admin_senha = db.Column(db.String(50), nullable=False)
class Categoria(db.Model):
    categoria_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria_descricao = db.Column(db.String(50), nullable=False)
    
    
 