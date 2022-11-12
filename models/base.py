from config import App 

db = App.get_db()

class Base(db.Model):
    __abstract__ = True