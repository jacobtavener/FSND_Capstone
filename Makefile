#!/bin/sh
# wait-for-postgres.sh

local_database: docker_up
	sleep 2
	flask db upgrade
	PGPASSWORD=hotel psql hotel_bookings <  src/database/hotel_data.psql -U postgres -h localhost -p 5433

local_psql:
	psql postgresql://postgres:hotel@localhost:5433/hotel_bookings

docker_up:
	docker-compose -f src/database/docker-compose.yml up -d

docker_down:
	docker-compose -f src/database/docker-compose.yml down

flask:
	python3 app.py

tests:
	python3 test_app.py
	PGPASSWORD=8c03bf02f174eefcd3af9fce3071de89b6b97ee050cb930f079c088596f16196 \
		psql d32ulf72a1cfan <src/database/test_rollback.psql -U ivvfjiktdpgpcc -h ec2-46-137-84-140.eu-west-1.compute.amazonaws.com -p 5432


