import os
import uuid

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *

from dates import booked_dates
from auth import requires_auth, AuthError


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

##GET REQUEST METHODS

  @app.route('/bookings')
  @requires_auth('get:bookings')
  def get_bookings(payload):
    try:
      bookings = Booking.query.all()
      booking = {str(b.uuid):\
                            {**b.booking(), **b.guest.booking(), **b.room.booking(), **b.room.roomtype.booking()}
                            for b in bookings}
      return jsonify({
        "success": True,
        "bookings": booking
      })
    except Exception:
      abort(500)

  @app.route('/roomtypes')
  @requires_auth('get:roomtypes')
  def get_room_types(payload):
    try:
      roomtypes = {"roomtype_id_"+str(r.id) : r.long()\
                    for r in RoomType.query.all()}
      
      return jsonify({
        "success": True,
        "Room Types": roomtypes
      })
    except Exception:
      abort(500)  

  @app.route('/guests')
  @requires_auth('get:guests')
  def get_guests(payload):
    try:
      booked_guests = [str(b.guest_uuid) for b in Booking.query.all()]
      guest_bookings = {id : {b.id : {**b.guest_view(), **b.room.booking()} for\
                        b in Booking.query.filter_by(guest_uuid = id).all()} \
                          for id in booked_guests}
      guests = {str(g.uuid) : g.long() for g in Guest.query.all()}
      for id in guests.keys():
        if id in booked_guests:
          guests[id]["bookings"] = guest_bookings[id]
        else:
          guests[id]["bookings"] = {}
      return jsonify({
        "success": True,
        "guests": guests
      })
    except Exception:
      abort(500)

  @app.route('/guests/<string:guest_uuid>')
  @requires_auth('get:guests_by_uuid')
  def get_guests_by_uuid(payload, guest_uuid):
    guest = Guest.query.filter_by(uuid = guest_uuid).one_or_none()
    if guest is None:
      abort(422, 'guest uuid not found')
    try:
      guest = guest.long()
      bookings = Booking.query.filter_by(guest_uuid= guest_uuid).all()
      if len(bookings) == 0:
        guest['bookings'] = {}
      else:
        guest['bookings'] = {str(b.uuid) : {**b.guest_view(), **b.room.booking()} for b in bookings}
      return jsonify({
        "success": True,
        "guest": guest
      })
    except Exception:
      abort(500)

  @app.route('/rooms')
  @requires_auth('get:rooms')
  def get_rooms(payload):
    try:
      rooms = {r.id : \
                {**r.booking(), **r.roomtype.long_no_id(), "dates_booked" : booked_dates(r)} \
                for r in Room.query.all()}
      
      return jsonify({
        "success": True,
        "rooms": rooms
      })
    except Exception:
      abort(500)

  @app.route('/rooms/<int:room_id>')
  @requires_auth('get:room_by_id')
  def get_room_by_id(payload, room_id):
    try:
      r = Room.query.filter_by(id = room_id).one_or_none()
      room = {**r.booking(), **r.roomtype.long_no_id(), "dates_booked" : booked_dates(r)}
      return jsonify({
        "success": True,
        "room": room
      })
    except Exception:
      abort(422, "room not found")

##POST REQUEST METHODS

  @app.route('/bookings', methods=["POST"])
  @requires_auth('post:booking')
  def create_booking(payload):
    
    data = request.get_json()
    if set(data.keys()) != set(Booking.params()):
      abort(400, "input parameter missing")

    try: 
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

      return jsonify({
        "success": True,
        "booking": booking
      }) 
    except Exception:
      abort(500)
    
  @app.route('/guests', methods=["POST"])
  @requires_auth('post:guests')
  def add_new_guest(payload):
    data = request.get_json()
    if set(data.keys()) != set(Guest.params()):
      abort(400, "input parameters missing")
    try:
      params = {
        "uuid" : uuid.uuid4(),
        "name" : data.get('name'),
        "mobile" : data.get('mobile'),
        "email" : data.get('email')
      }
      new_guest = Guest(**params)
      Guest.insert(new_guest)
      guest = new_guest.long()
      return jsonify({
        "success": True,
        "guest": guest
      })
    except Exception:
      abort(500)

##PATCH REQUEST METHODS

  @app.route('/bookings/<string:booking_uuid>', methods=["PATCH"])
  @requires_auth('patch:booking')
  def edit_bookings(payload, booking_uuid):
    data = request.get_json()
    booking = Booking.query.filter_by(uuid = booking_uuid).one_or_none()
    if booking is None:
      abort(422, "booking not found")
    try:
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
      return jsonify({
        "success": True,
        "booking": booking.long()
      })
    except Exception:
      abort(500)


  @app.route('/guests/<string:guest_uuid>', methods=["PATCH"])
  @requires_auth('patch:guest')
  def edit_guest(payload, guest_uuid):
    data = request.get_json()
    guest = Guest.query.filter_by(uuid = guest_uuid).one_or_none()
    if guest is None:
      abort(422, "guest not found")
    try:
      if "name" in data:
        guest.name = data.get("name")
      if "mobile" in data:
        guest.mobile = data.get("mobile")
      if "email" in data:
        guest.email = data.get("email")
      Guest.update(guest)
      return jsonify({
        "success": True,
        "guest": guest.long()
      })
    except Exception:
      abort(500)

##DELETE REQUEST METHODS

  @app.route('/bookings/<string:booking_uuid>', methods=["DELETE"])
  @requires_auth('delete:booking')
  def remove_booking(payload, booking_uuid):
    booking = Booking.query.filter_by(uuid = booking_uuid).one_or_none()
    if booking is None:
      abort(422, "booking not found")
    try:
      Booking.delete(booking)
      return jsonify({
        "success": True,
        "booking_uuid": booking_uuid
        })
    except Exception:
      abort(500)

  @app.route('/guests/<string:guest_uuid>', methods=["DELETE"])
  @requires_auth('delete:guest')
  def remove_guests(payload, guest_uuid):
    guest = Guest.query.filter_by(uuid = guest_uuid).one_or_none()
    if guest is None:
      abort(422, "guest not found")
    try:
      name = guest.name
      for booking in Booking.query.filter_by(guest_uuid = guest_uuid).all():
        Booking.delete(booking)
      Guest.delete(guest)

      return jsonify({
        "success": True,
        "guest_uuid" : guest_uuid,
        "removed": name
        })
    except Exception:
      abort(500)

#ERROR HANDLING

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": error.description
      }), 422


  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": error.description
      }), 400


  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": error.description
      }), 500

  @app.errorhandler(AuthError)
  def authentication_error(e):
      return jsonify(e.error), e.status_code  
    
  return app

  
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0' , port=8080, debug=True)