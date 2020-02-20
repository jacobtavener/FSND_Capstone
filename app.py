import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from dates import booked_dates

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
    booking = {"booking_id_"+str(b.id):\
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

    booked_guests = [b.guest_id for b in Booking.query.all()]
    guest_bookings = {id : {b.id : {**b.guest_view(), **b.room.booking()} for\
                       b in Booking.query.filter_by(guest_id = id).all()} \
                         for id in booked_guests}

    guests = {g.id : g.long() for g in Guest.query.all()}

    for id in guests.keys():
      if id in booked_guests:
        guests[id]["zbookings"] = guest_bookings[id]
      else:
        guests[id]["zbookings"] = {}
    return jsonify(guests)

  @app.route('/guests/<int:guest_id>')
  def get_guests_by_id(guest_id):
    guest = Guest.query.filter_by(id = guest_id).one_or_none()
    if guest is None:
      return jsonify({
        "error":"guest id not found"
      })

    else:
      guest = guest.long()
      bookings = Booking.query.filter_by(id= guest_id).all()
      
      if len(bookings) == 0:
        guest['bookings'] = {}
      else:
        guest['bookings'] = {b.id : {**b.guest_view(), **b.room.booking()} for b in bookings}
      
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

  # @app.route('/bookings', METHODS=["POST"])
  # def create_booking():
    
  #   data = request.get_json()
  #   expected_parameters = ["room_id"]

    



  @app.route('/testing')
  def tests():

    bookings = [b.guest_view() for b in Booking.query.all()]
  
    room = Room.query.first()
    dates_booked=booked_dates(room)



    return jsonify({
      "bookings":dates_booked
    })


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0' , port=8080, debug=True)