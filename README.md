# FSND Hotel Project 
## capstone project for udacit full stack nanodegree program

## Heroku Link .... https://capstone-hotel-app.herokuapp.com/ | https://git.heroku.com/capstone-hotel-app.git

## Motivation
This api purpose is to be used internally within a small hotel.
It acts a central location for all information regarding, rooms, guests and bookings.
Its use is aimed at:
- Hotel Managers
    - to oversee the whole operation and have full access to functionality
- Receptionists
    - in order to access, edit and create new bookings or guest profiles
- Hotel restaurant staff
    - to help regulate the access to the breakfast facilities

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the '/' directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in api.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Running the Server

To run the server with your own database connection, execute:

```
make custom_flask
```

To run the server using the dockerised postgres sample database, execute:

```
make flask
```

you will need to provide the password 'hotel' upon request.

if you use this sample database, when you end the flask session, please ensure you then excute:

```
make down
```

this stops the container from running.

### Running the tests
The tests have be configured to run in conjunction with the data in the sample database provided.
In order to run the tests:
1. ensure you have the server running in the ```make flask ``` set up
2. In a seperate terminal, provided you are in the directory and have reactivated the env, the tests will run by executing 
    ```make test```

### Models
##### Guests
Attributes:

- ID
- UUID
- Name
- Email
- Mobile

##### Rooms
Attributes:

- ID
- Type ID

##### Room Types
Attributes:

- ID
- Name 
- Type 
- View
- Description

##### Bookings
Attributes:
- ID 
- UUID 
- Room uuid
- Guest uuid
- Date in 
- Date out
- Breakfast
- Paid 
- Reason for stay 

### Roles

##### Restaurant Manager
- GET:bookings

##### Receptionist
All permissions a Restaurant Manager has as well as:

- GET:guests
- GET:guests_by_uuid
- GET:rooms
- GET:rooms_by_id
- GET:roomtypes

- PATCH:booking
- PATCH:guest

- POST:booking
- POST:guests

##### Hotel Manager
All permissions a Receptionist has as well as:

- DELETE:booking
- DELETE:guest

### Environment Variables 
In the ```.env``` file, there are 4 JWT tokens, 3 for the different users holding different roles & 1 expired token for testing purposes

- HOTEL_MANAGER
- RECEPTION
- RESTAURANT MANAGER
- EXPIRED_TOKEN

### Endpoints 

``` 
GET '/bookings'

The bookings have the UUID as keys to enable quick searching in future 

response = {
        "success": True,
        "bookings": {
            "07edecf2-5567-11ea-84a8-acde48001122": {
                "booking_id": "07edecf2-5567-11ea-84a8-acde48001122",
                "breakfast": true,
                "date_in": "Wed, 12 Feb 2020 00:00:00 GMT",
                "date_out": "Sun, 16 Feb 2020 00:00:00 GMT",
                "name": "double",
                "paid": true,
                "price": 100,
                "reason for stay": "business",
                "room_number": 1
            },
            "2f3030a4-5567-11ea-84a8-acde48001122": {
                "booking_id": "2f3030a4-5567-11ea-84a8-acde48001122",
                "breakfast": false,
                "date_in": "Wed, 29 Apr 2020 00:00:00 GMT",
                "date_out": "Mon, 18 May 2020 00:00:00 GMT",
                "name": "single",
                "paid": true,
                "price": 60,
                "reason for stay": "pleasure",
                "room_number": 2
            }
        }
    }
```

```
GET '/roomtypes'

response = {
  "Room Types": {
    "roomtype_id_1": {
      "description": "one bed suitable for single guest",
      "id": 1,
      "name": "single",
      "price": 60,
      "view": "sea"
    },
    "roomtype_id_2": {
      "description": "suitable for couples or pairs",
      "id": 2,
      "name": "double",
      "price": 100,
      "view": "street"
    }
  },
  "success": true
}
```

```
GET '/guests'

The guests have the UUID as keys to enable fast searching in the future
Also returns a dict of the booking belonging to each guest.

response = {
        "guests": {
                "8ede78bc-5567-11ea-84a8-acde48001122": {
                "bookings": {
                    "1": {
                    "booking_id": "07edecf2-5567-11ea-84a8-acde48001122",
                    "date_in": "Wed, 12 Feb 2020 00:00:00 GMT",
                    "date_out": "Sun, 16 Feb 2020 00:00:00 GMT",
                    "room_number": 1
                    }
                },
                "email": "jacob@email.com",
                "id": 1,
                "mobile": "07754354292",
                "name": "jacob",
                "uuid": "8ede78bc-5567-11ea-84a8-acde48001122"
                }
            },
            "success": True 
        }  
```

``` 
GET '/guests/<string:guest_uuid>'

example: guests/

response = {
    "guest": {
        "bookings": {
        "07edecf2-5567-11ea-84a8-acde48001122": {
            "booking_id": "07edecf2-5567-11ea-84a8-acde48001122",
            "date_in": "Wed, 12 Feb 2020 00:00:00 GMT",
            "date_out": "Sun, 16 Feb 2020 00:00:00 GMT",
            "room_number": 1
        }
        },
        "email": "jacob@email.com",
        "id": 1,
        "mobile": "07754354292",
        "name": "jacob",
        "uuid": "8ede78bc-5567-11ea-84a8-acde48001122"
    },
    "success": true
}
```

```
GET '/rooms' 

response = {
    "rooms": {
        "1": {
        "dates_booked": [
            "Wed, 12 Feb 2020 00:00:00 GMT",
            "Thu, 13 Feb 2020 00:00:00 GMT",
            "Fri, 14 Feb 2020 00:00:00 GMT",
            "Sat, 15 Feb 2020 00:00:00 GMT",
            "Sun, 16 Feb 2020 00:00:00 GMT",
            "Mon, 23 Mar 2020 00:00:00 GMT",
            "Tue, 24 Mar 2020 00:00:00 GMT"
        ],
        "description": "suitable for couples or pairs",
        "name": "double",
        "price": 100,
        "room_number": 1,
        "view": "street"
        },
        "2": {
        "dates_booked": [
            "Wed, 29 Apr 2020 00:00:00 GMT",
            "Thu, 30 Apr 2020 00:00:00 GMT",
            "Fri, 01 May 2020 00:00:00 GMT",
            "Sat, 02 May 2020 00:00:00 GMT",
            "Sun, 03 May 2020 00:00:00 GMT",
            "Mon, 04 May 2020 00:00:00 GMT",
            "Tue, 05 May 2020 00:00:00 GMT",
            "Wed, 06 May 2020 00:00:00 GMT",
            "Thu, 07 May 2020 00:00:00 GMT",
            "Fri, 08 May 2020 00:00:00 GMT",
            "Sat, 09 May 2020 00:00:00 GMT",
            "Sun, 10 May 2020 00:00:00 GMT",
            "Mon, 11 May 2020 00:00:00 GMT",
            "Tue, 12 May 2020 00:00:00 GMT",
            "Wed, 13 May 2020 00:00:00 GMT",
            "Thu, 14 May 2020 00:00:00 GMT",
            "Fri, 15 May 2020 00:00:00 GMT",
            "Sat, 16 May 2020 00:00:00 GMT",
            "Sun, 17 May 2020 00:00:00 GMT",
            "Mon, 18 May 2020 00:00:00 GMT",
            "Fri, 21 Feb 2020 00:00:00 GMT",
            "Sat, 22 Feb 2020 00:00:00 GMT",
            "Sun, 23 Feb 2020 00:00:00 GMT",
            "Mon, 24 Feb 2020 00:00:00 GMT",
            "Tue, 25 Feb 2020 00:00:00 GMT",
            "Wed, 26 Feb 2020 00:00:00 GMT"
        ],
        "description": "one bed suitable for single guest",
        "name": "single",
        "price": 60,
        "room_number": 2,
        "view": "sea"
        }
    },
    "success": true
    }
```

```
GET '/rooms/<int:room_id>'

example = '/rooms/1'

response = {
    "room": {
        "dates_booked": [
        "Wed, 12 Feb 2020 00:00:00 GMT",
        "Thu, 13 Feb 2020 00:00:00 GMT",
        "Fri, 14 Feb 2020 00:00:00 GMT",
        "Sat, 15 Feb 2020 00:00:00 GMT",
        "Sun, 16 Feb 2020 00:00:00 GMT",
        "Mon, 23 Mar 2020 00:00:00 GMT",
        "Tue, 24 Mar 2020 00:00:00 GMT"
        ],
        "description": "suitable for couples or pairs",
        "name": "double",
        "price": 100,
        "room_number": 1,
        "view": "street"
    },
    "success": true
    }
```

```
POST '/bookings'

payload = {
            "room_id": 2,
            "guest_uuid" : "c5ef43fe-5567-11ea-84a8-acde48001122",
            "date_in" : "2020-04-27",
            "date_out" : "2020-05-03",
            "breakfast" : true,
            "paid" : true,
            "reason_for_stay" : "business"
        }

response = {
            "booking": {
                "breakfast": true,
                "date_in": "Mon, 27 Apr 2020 00:00:00 GMT",
                "date_out": "Sun, 03 May 2020 00:00:00 GMT",
                "guest_uuid": "c5ef43fe-5567-11ea-84a8-acde48001122",
                "id": 5,
                "paid": true,
                "reason for stay": "business",
                "room_id": 2,
                "uuid": "5a37626e-c13f-4f7e-a261-be86b257bd9c"
            },
            "success": true
        }    
```

```
POST '/guests'

payload = {
            "name" : "Vito",
            "mobile" : "0775848392",
            "email" : "vito@email.com"
        }

response = {
            "guest": {
                "email": "vito@email.com",
                "id": 6,
                "mobile": "0775848392",
                "name": "Vito",
                "uuid": "3fa2ee75-33e3-4867-a32b-499819e70f69"
            },
            "success": true
        }
```

```
PATCH 'bookings/<string:booking_uuid>'

example :  'bookings/2f3030a4-5567-11ea-84a8-acde48001122'

payload = {
            "breakfast" : true
        }

response = {
            "booking": {
                "breakfast": true,
                "date_in": "Wed, 29 Apr 2020 00:00:00 GMT",
                "date_out": "Mon, 18 May 2020 00:00:00 GMT",
                "guest_uuid": "90376688-5567-11ea-84a8-acde48001122",
                "id": 2,
                "paid": true,
                "reason for stay": "pleasure",
                "room_id": 2,
                "uuid": "2f3030a4-5567-11ea-84a8-acde48001122"
            },
            "success": true
        }
```

``` 
PATCH '/guests/<string:guest_uuid>'

example : '/guests/91242f0e-5567-11ea-84a8-acde48001122'

payload = {
            "email":"email@herbie.com"	
        }

response = {
            "guest": {
                "email": "email@herbie.com",
                "id": 4,
                "mobile": "07583821",
                "name": "herbie",
                "uuid": "91242f0e-5567-11ea-84a8-acde48001122"
            },
            "success": true
        }
```

```
DELETE '/bookings/<string:booking_uuid>'

example '/bookings/2f4030a4-5567-11ea-84a8-acde48001122'

response = {
            "booking_uuid": "07edecf2-5567-11ea-84a8-acde48001122",
            "success": true
            }
```

```
DELETE '/guests/<string:guest_uuid>'

This deletes the guest and all of their bookings 

example '/guests/8ede78bc-5567-11ea-84a8-acde48001122'

response = {
            "guest_uuid": "8ede78bc-5567-11ea-84a8-acde48001122",
            "removed": "jacob",
            "success": true
        }
```

