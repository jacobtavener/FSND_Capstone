#!/bin/sh
# wait-for-postgres.sh

flask: up
	sleep 2
	flask db upgrade
	psql hotel_bookings <  hotel_data.psql -U postgres -h localhost -p 5433
	python3 app.py

psql:
	psql postgresql://postgres:hotel@localhost:5433/hotel_bookings

up:
	docker-compose up -d

down:
	docker-compose down

tests:
	python3 unittests.py

custom_flask:
	python3 app.py
