import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *

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

  @app.route('/')
  def test():
    booking = Booking.query.one()
    test = booking.guest.name
  
    return jsonify({
      'test': test
    })

  return app


  
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0' , port=8080, debug=True)