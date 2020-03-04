import datetime
import os
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, create_engine,\
                        ForeignKey, ARRAY, Date, Boolean, types
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from sqlalchemy.orm import relationship
from dotenv import load_dotenv

load_dotenv()

database_path = os.environ['DATABASE_URL']

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
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(String)
    mobile = Column(String)
    email = Column(String)
    bookings = relationship('Booking', backref='guest', lazy=True)

    def __init__(self, uuid, name, mobile, email):
        self.uuid = uuid
        self.name =  name 
        self.mobile = mobile
        self.email = email

    def long(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email
        }
    def booking(self):
        return{
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
        return json.dumps(self.long())

    @classmethod
    def params(cls):
        parameters = ['name', 'mobile', 'email']
        return parameters    

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

    def booking(self):
        return {
            'name': self.name,
            'price': self.price
        }
    
    def long_no_id(self):
        return {
        'name': self.name,
        'price': self.price,
        'view': self.view,
        'description': self.description
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
        return json.dumps(self.long())

class Room(db.Model):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('room_types.id'), nullable=False)
    bookings = relationship('Booking', backref='room', lazy=True)


    def __init__(self, type_id, dates_booked):
        self.type_id = type_id
        self.dates_booked = dates_booked

    def long(self):
        return {
        'id': self.id,
        'type_id': self.type_id
        }
    
    def booking(self):
        return {
        'room_number': self.id,
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
        return json.dumps(self.long()) 

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    guest_uuid = Column(UUID(as_uuid=True), ForeignKey('guests.uuid'), nullable=False)
    date_in = Column(Date)
    date_out = Column(Date)
    breakfast = Column(Boolean)
    paid = Column(Boolean)
    reason_for_stay = Column(String)

    def __init__(self, uuid, room_id, guest_uuid, date_in, date_out, breakfast, paid, reason_for_stay):
        self.uuid = uuid
        self.room_id = room_id
        self.guest_uuid = guest_uuid
        self.date_in = date_in
        self.date_out = date_out
        self.breakfast = breakfast
        self.paid = paid
        self.reason_for_stay = reason_for_stay


    def long(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'room_id': self.room_id,
            'guest_uuid': self.guest_uuid,
            'date_in': self.date_in,
            'date_out': self.date_out,
            'breakfast': self.breakfast,
            'paid': self.paid,
            'reason for stay': self.reason_for_stay
        }
    
    def booking(self):
        return {
            'booking_id': self.uuid,
            'date_in': self.date_in,
            'date_out': self.date_out,
            'breakfast': self.breakfast,
            'paid': self.paid,
            'reason for stay': self.reason_for_stay
        }
    
    def guest_view(self):
        return {
            'booking_id': self.uuid,
            'date_in': self.date_in,
            'date_out': self.date_out
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
        return json.dumps(self.long())

    @classmethod
    def params(cls):
        parameters = ['room_id', 'guest_uuid', 'date_in', \
                         'date_out', 'breakfast', 'paid', 'reason_for_stay'] 
        return parameters

# Extra helper functions

def booked_dates(room):
    bookings = Booking.query.filter_by(room_id = room.id).all()
    booked=[]
    for booking in bookings:
        start = booking.date_in
        end = booking.date_out
        booked += all_dates(start, end)
    return booked


def all_dates(start, end):
    diff = end - start
    dates = [start + datetime.timedelta(days=i) for i in range(diff.days+1)]
    return dates
        
def is_available(room, start_date, end_date):

    potential_dates = all_dates(start_date, end_date)
    dates_booked = booked_dates(room)

    if set(potential_dates).isdisjoint(set(dates_booked)):
        return True
    else:
        return False
