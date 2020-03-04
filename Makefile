#!/bin/sh
# wait-for-postgres.sh

local_flask: up
	sleep 2
	flask db upgrade
	psql hotel_bookings <  hotel_data.psql -U postgres -h localhost -p 5433
	python3 app.py

local_psql:
	psql postgresql://postgres:hotel@localhost:5433/hotel_bookings

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

local_tests:
	python3 unittests.py

heroku_flask:
	python3 app.py
