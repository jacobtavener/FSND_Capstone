import os
from sqlalchemy import Column, String, Integer, create_engine,\
                        ForeignKey, ARRAY, Date, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from sqlalchemy.orm import relationship

database_name = "hotel_bookings"
database_path = "postgresql://{}:{}@{}/{}".format('postgres','hotel', 'localhost:5433', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    migrate = Migrate(app, db)


class Guest(db.Model):  
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = Column(String)
    email = Column(String)
    reason_for_stay = Column(String)
    bookings = relationship('Booking', backref='guest', lazy=True)

    def __init__(self, name, mobile, email, reason_for_stay):
        self.name =  name 
        self.mobile = mobile
        self.email = email
        self.reason_for_stay = reason_for_stay

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email,
            'reason_for_stay': self.reason_for_stay
        }
    def short(self):
        return{
            'id': self.id,
            'name': self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())    

class RoomType(db.Model):
    __tablename__ = 'room_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    view = Column(String)
    description = Column(String)
    rooms = relationship('Room', backref='roomtype', lazy=True)


    def __init__(self, name, price, view, description):
        self.name =  name 
        self.price = price
        self.view = view
        self.description = description

    def long(self):
        return {
        'id': self.id,
        'name': self.name,
        'price': self.price,
        'view': self.view,
        'description': self.description
        }

    def short(self):
        return {
            'name': self.name,
            'price': self.price
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


class Room(db.Model):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('room_types.id'), nullable=False)
    dates_booked = Column(ARRAY(Date))
    bookings = relationship('Booking', backref='room', lazy=True)


    def __init__(self, type_id, dates_booked):
        self.type_id = type_id
        self.dates_booked = dates_booked

    def long(self):
        return {
        'id': self.id,
        'dates_booked': self.dates_booked,
        'type_id': self.type_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format()) 

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    guest_id = Column(Integer, ForeignKey('guests.id'), nullable=False)
    date_in = Column(Date)
    date_out = Column(Date)
    breakfast = Column(Boolean)
    paid = Column(Boolean)

    def __init__(self, room_id, guest_id, date_in, date_out, breakfast, paid):
        self.room_id = room_id
        self.guest_id = guest_id
        self.date_in = date_in
        self.date_out = date_out
        self.breakfast = breakfast
        self.paid = paid


    def long(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'guest_id': self.guest_id,
            'date_in': self.date_in,
            'date_out': self.date_out,
            'breakfast': self.breakfast,
            'paid': self.paid
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())
