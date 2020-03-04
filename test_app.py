import os
import unittest
import json
import uuid

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from app import APP
from src.database.models import setup_db, Room, Guest, RoomType, Booking, db

load_dotenv()


class HotelTestCase(unittest.TestCase):
    """ This class represents the Hotel test case """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.hotel_manager = os.getenv("HOTEL_MANAGER")
        self.receptionist = os.getenv("RECEPTION")
        self.restaurant = os.getenv("RESTAURANT_MANAGER")
        self.expired_token = os.getenv("EXPIRED_TOKEN")
        self.database_path = os.getenv('DATABASE_URL')
        setup_db(self.app, self.database_path)

        # add sample data to be used in the tests
        self.new_booking = {
            'room_id': 2,
            'guest_uuid': 'c5ef43fe-5567-11ea-84a8-acde48001122',
            'date_in': '2020-06-05',
            'date_out': '2020-06-08',
            'breakfast': True,
            'paid': False,
            'reason_for_stay': 'business'
        }
        self.failed_new_booking = {
            'guest_uuid': 'c5ef43fe-5567-11ea-84a8-acde48001122',
            'date_in': '2020-06-05',
            'date_out': '2020-06-08',
            'breakfast': True,
            'paid': False,
            'reason_for_stay': 'business'
        }
        self.new_guest = {
            "name": 'Vito',
            "mobile": '08674782029',
            "email": 'email@email.com'
        }
        self.failed_new_guest = {
            "mobile": '08674782029',
            "email": 'email@email.com'
        }
        self.edit_booking = {
            'reason_for_stay': 'pleasure'
        }
        self.edit_guest = {
            'name': "Rosie"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TESTING GET ENDPOINTS
    """

    def test_get_bookings(self):
        res = self.client().get('/bookings', headers={
            "Authorization": "Bearer {}".format(
                self.restaurant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['bookings'])

    def test_get_roomtypes(self):
        res = self.client().get('/roomtypes', headers={
            "Authorization": "Bearer {}".format(
                self.hotel_manager)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Room Types'])

    def test_401_unauthorized_get_roomtypes(self):
        res = self.client().get('/roomtypes', headers={
            "Authorization": "Bearer {}".format(
                self.restaurant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not permitted to use this feature")

    def test_get_guests(self):
        res = self.client().get('/guests', headers={
            "Authorization": "Bearer {}".format(
                self.receptionist)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['guests'])

    def test_401_no_jwt_guests(self):
        res = self.client().get('/guests')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "no JWT provided")

    def test_get_guests_by_uuid(self):
        res = self.client().get(
            '/guests/8ede78bc-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.receptionist)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['guest'])

    def test_422_guest_uuid_not_found(self):
        res = self.client().get('/guests/1f3a0d7c-5969-11ea-bcd5-acde48001122',
                                headers={"Authorization": "Bearer {}".format(self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "guest uuid not found")

    def test_get_rooms(self):
        res = self.client().get('/rooms', headers={
            "Authorization": "Bearer {}".format(
                self.hotel_manager)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['rooms'])

    def test_get_rooms_by_id(self):
        res = self.client().get('/rooms/1', headers={
            "Authorization": "Bearer {}".format(
                self.hotel_manager)
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['room'])

    def test_422_room_not_exist(self):
        res = self.client().get('/rooms/1000', headers={
            "Authorization": "Bearer {}".format(
                self.hotel_manager)
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'room not found')

    """
    TESTING POST ENDPOINTS
    """

    def test_new_booking(self):
        res = self.client().post('/bookings', json=self.new_booking, headers={
            "Authorization": "Bearer {}".format(
                self.hotel_manager)
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['booking'])

    def test_400_failed_new_booking(self):
        res = self.client().post(
            '/bookings',
            json=self.failed_new_booking,
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "input parameter missing")

    def test_401_expired_token(self):
        res = self.client().post('/bookings', json=self.new_booking, headers={
            "Authorization": "Bearer {}".format(
                self.expired_token)
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'], "token_expired")
        self.assertTrue(data['description'], "Token expired.")

    def test_new_guest(self):
        res = self.client().post('/guests', json=self.new_guest, headers={
            "Authorization": "Bearer {}".format(
                self.receptionist)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['guest'])

    def test_400_failed_new_guest(self):
        res = self.client().post(
            '/guests',
            json=self.failed_new_guest,
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "input parameters missing")

    """
    TESTING PATCH ENDPOINTS
    """

    def test_edit_bookings(self):
        res = self.client().patch(
            '/bookings/07edecf2-5567-11ea-84a8-acde48001122',
            json=self.edit_booking,
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['booking']['reason for stay'], 'pleasure')
        self.assertTrue(data['booking'])

    def test_421_booking_uuid_not_found(self):
        res = self.client().patch(
            '/bookings/3fa63b8c-5567-11ea-84a8-acde48001122',
            json=self.edit_booking,
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'booking not found')

    def test_edit_guest(self):
        res = self.client().patch(
            '/guests/8f52bfc4-5567-11ea-84a8-acde48001122',
            json=self.edit_guest,
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['guest']['name'], 'Rosie')
        self.assertTrue(data['guest'])

    """
    TESTING DELETE ENDPOINTS
    """

    def test_delete_booking(self):
        res = self.client().delete(
            '/bookings/2f3030a4-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['booking_uuid'])

    def test_422_delete_booking_invalid_uuid(self):
        res = self.client().delete(
            '/bookings/2f4030a4-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'booking not found')

    def test_401_delete_booking_unauthorized(self):
        res = self.client().delete(
            '/bookings/07edecf2-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.receptionist)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not permitted to use this feature")

    def test_delete_guest(self):
        res = self.client().delete(
            '/guests/91242f0e-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['removed'])

    def test_422_delete_guest_invalid_uuid(self):
        res = self.client().delete(
            '/guests/c6ef43fe-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.hotel_manager)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'guest not found')

    def test_401_delete_guest_unauthorized(self):
        res = self.client().delete(
            '/guests/8ede78bc-5567-11ea-84a8-acde48001122',
            headers={
                "Authorization": "Bearer {}".format(
                    self.restaurant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not permitted to use this feature")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
