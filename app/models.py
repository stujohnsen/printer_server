from app import db

class Printer_info(db.Model):
    __tablename__ = 'info'
    
    printer_id = db.Column(db.Integer, primary_key = True)  # @UndefinedVariable
    x_api_key = db.Column(db.String(128))  # @UndefinedVariable
    ip_address = db.Column(db.String(60))  # @UndefinedVariable