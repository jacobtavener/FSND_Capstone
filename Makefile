#!/bin/sh
# wait-for-postgres.sh

local_database: docker_up
	sleep 2
	flask db init
	flask db upgrade
	psql hotel_bookings <  src/database/hotel_data.psql -U postgres -h localhost -p 5433

local_psql:
	psql postgresql://postgres:hotel@localhost:5433/hotel_bookings

docker_up:
	docker-compose -f src/database/docker-compose.yml up -d

docker_down:
	docker-compose -f src/database/docker-compose.yml down
	rm -rf migrations/

local_flask:
	python3 app.py

tests:
	python3 test_app.py