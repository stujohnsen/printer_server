from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Printer_db(Base):
    __tablename__ = 'printers'

    printer_id = Column(Integer, primary_key = True)
    url = Column(String(512))
    x_api_key = Column(String(512))
    camera_rotation = Column(Integer)
    printer_name = Column(String(512))
    printer_type = Column(String(512))
    horizontal_flip = Column(Boolean)
    vertical_flip = Column(Boolean)

    def __repr__(self):
        return '<Printer_info %r>' % self.printer_id

    # @classmethod
    # def get_printer_id_list(self):
    #     result = []
    #     printer_list = Printer_db.query.order_by(Printer_db.printer_id).all()
    #     for p in printer_list:
    #         result.append(str(p.printer_id))
    #     return result
    #
    # @classmethod
    # def get_url(self, printer_id):
    #     printer = Printer_db.query.filter_by(printer_id=printer_id).first()
    #     return str(printer.url)
    #
    # @classmethod
    # def get_x_api_key(self, printer_id):
    #     printer = Printer_db.query.filter_by(printer_id=printer_id).first()
    #     return str(printer.x_api_key)
    #
    # @classmethod
    # def get_camera_rotation_angle(self, printer_id):
    #     printer = Printer_db.query.filter_by(printer_id=printer_id).first()
    #     return str(printer.camera_rotation)

    @classmethod
    def get_on_startup(self):
        result = {}
        printer_list = Printer_db.query.order_by(Printer_db.printer_id).all()
        for p in printer_list:
            info = {'printer_id': str(p.printer_id),
                    'url': str(p.url),
                    'x_api_key': str(p.x_api_key),
                    'camera_rotation': str(p.camera_rotation),
                    'printer_name': str(p.printer_name),
                    'printer_type': str(p.printer_type),
                    'horizontal_flip' : str(p.horizontal_flip),
                    'vertical_flip' : str(p.vertical_flip),
                    }
            result[str(p.printer_id)] = info
        return result

# this code has been commented out for security reasons
# in the running version, it contains the database connection info
# This code normally connects via a python config file with the appropriate information
# the config file has also been omitted from our solution for security reasons
engine = create_engine('REPLACE THIS WITH DATABASE INFORMATION', echo=False)
printers_table = Printer_db.__table__
metadata = Base.metadata
metadata.create_all(engine)

def get_on_startup():
    result = {}
    printer_list = Printer_db.query.order_by(Printer_db.printer_id).all()
    for p in printer_list:
        info = { 'printer_id' : str(p.printer_id),
                 'url': str(p.url),
                 'x_api_key' : str(p.x_api_key),
                 'camera_rotation' : str(p.camera_rotation),
                 'printer_name' : str(p.printer_name),
                 'printer_type' : str(p.printer_type),
                 'horizontal_flip' : str(p.horizontal_flip),
                 'vertical_flip' : str(p.vertical_flip),
                }
        result[str(p.printer_id)] = info
    return result
