import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from dates import booked_dates
import uuid

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)
  CORS(app, resources={r"/capstone/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

##GET ENDPOINTS

  @app.route('/bookings')
  def get_bookings():

    bookings = Booking.query.all()
    booking = {str(b.uuid):\
                          {**b.booking(), **b.guest.booking(), **b.room.booking(), **b.room.roomtype.booking()}
                          for b in bookings}

    return jsonify(booking)

  @app.route('/roomtypes')
  def get_room_types():

    roomtypes = {"roomtype_id_"+str(r.id) : r.long()\
                  for r in RoomType.query.all()}
    
    return jsonify(roomtypes)  

  @app.route('/guests')
  def get_guests():

    booked_guests = [str(b.guest_uuid) for b in Booking.query.all()]
    guest_bookings = {id : {b.id : {**b.guest_view(), **b.room.booking()} for\
                       b in Booking.query.filter_by(guest_uuid = id).all()} \
                         for id in booked_guests}

    guests = {str(g.uuid) : g.long() for g in Guest.query.all()}

    for id in guests.keys():
      if id in booked_guests:
        guests[id]["zbookings"] = guest_bookings[id]
      else:
        guests[id]["zbookings"] = {}
    return jsonify(guests)

  @app.route('/guests/<string:guest_uuid>')
  def get_guests_by_uuid(guest_uuid):
    guest = Guest.query.filter_by(uuid = guest_uuid).one_or_none()
    if guest is None:
      return jsonify({
        "error":"guest uuid not found"
      })

    else:
      guest = guest.long()
      bookings = Booking.query.filter_by(guest_uuid= guest_uuid).all()
      
      if len(bookings) == 0:
        guest['bookings'] = {}
      else:
        guest['bookings'] = {str(b.uuid) : {**b.guest_view(), **b.room.booking()} for b in bookings}
      
      return jsonify(guest)

  @app.route('/rooms')
  def get_rooms():

    rooms = {r.id : \
              {**r.booking(), **r.roomtype.long_no_id(), "dates_booked" : booked_dates(r)} \
              for r in Room.query.all()}
    
    return jsonify(rooms)

  @app.route('/rooms/<int:room_id>')
  def get_room_by_id(room_id):
    r = Room.query.filter_by(id = room_id).one_or_none()
    if r is None:
      return jsonify({})

    else:
      room = {**r.booking(), **r.roomtype.long_no_id(), "dates_booked" : booked_dates(r)}

      return jsonify(room)

##POST ENDPOINTS

  @app.route('/bookings', methods=["POST"])
  def create_booking():
    
    data = request.get_json()
    if set(data.keys()) != set(Booking.params()):
      return jsonify(
        {}
      )

    else: 
      params ={
      'uuid' : uuid.uuid4(),
      'room_id' : data.get('room_id'),
      'guest_uuid' : data.get('guest_uuid'),
      'date_in' : data.get('date_in'),
      'date_out' : data.get('date_out'),
      'breakfast' : data.get('breakfast'),
      'paid' : data.get('paid'),
      'reason_for_stay' : data.get('reason_for_stay')
      }

      new_booking = Booking(**params)
      Booking.insert(new_booking)

      booking = new_booking.long()

      return jsonify(booking)

  @app.route('/guests', methods=["POST"])
  def add_new_guest():

    data = request.get_json()

    if set(data.keys()) != set(Guest.params()):
      return jsonify({})

    else:
      params = {
        "uuid" : uuid.uuid1(),
        "name" : data.get('name'),
        "mobile" : data.get('mobile'),
        "email" : data.get('email')
      }

      new_guest = Guest(**params)
      Guest.insert(new_guest)

      guest = new_guest.long()

      return jsonify(guest)

##PATCH ENDPOINTS

  @app.route('/bookings/<string:booking_uuid>', methods=["PATCH"])
  def edit_bookings(booking_uuid):

    data = request.get_json()
    booking = Booking.query.filter_by(uuid = booking_uuid).one_or_none()

    if booking is None:
      return jsonify({})

    else:
      if "room_id" in data:
        booking.room_id = data.get("room_id")

      if "guest_uuid" in data:
        booking.guest_uuid = data.get("guest_uuid")

      if "date_in" in data:
        booking.date_in = data.get("date_in")

      if "date_out" in data:
        booking.date_out = data.get("date_out")

      if "breakfast" in data: 
        booking.breakfast = data.get("breakfast")

      if "paid" in data:
        booking.paid = data.get("paid")

      if "reason_for_stay" in data:
        booking.reason_for_stay = data.get("reason_for_stay")

      Booking.update(booking)

      return jsonify(booking.long())

  @app.route('/guests/<string:guest_uuid>', methods=["PATCH"])
  def edit_guest(guest_uuid):
    
    data = request.get_json()
    guest = Guest.query.filter_by(uuid = guest_uuid).one_or_none()

    if guest is None:
      return jsonify({})

    else:
      if "name" in data:
        guest.name = data.get("name")

      if "mobile" in data:
        guest.mobile = data.get("mobile")

      if "email" in data:
        guest.email = data.get("email")


      Guest.update(guest)

      return jsonify(guest.long())
    
##DELETE ENDPOINTS

  @app.route('/bookings/<string:booking_uuid>', methods=["DELETE"])
  def remove_booking(booking_uuid):
    booking = Booking.query.filter_by(uuid = booking_uuid).one_or_none()
    if booking is None:
      return jsonify({})
    Booking.delete(booking)
    return jsonify({"booking_uuid": booking_uuid})

  @app.route('/guests/<string:guest_uuid>', methods=["DELETE"])
  def remove_guests(guest_uuid):
    guest = Guest.query.filter_by(uuid = guest_uuid).one_or_none()
    if guest is None:
      return jsonify({})
    name = guest.name
    Guest.delete(guest)
    return jsonify({"removed":name})

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0' , port=8080, debug=True)