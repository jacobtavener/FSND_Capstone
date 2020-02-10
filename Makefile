set_up:
	docker-compose up -d
	sleep 1
	python3 app.py

dump: 
	psql hotel_bookings <  hotel_data.psql -U postgres -h localhost -p 5433

psql:
	psql postgresql://postgres:hotel@localhost:5433/hotel_bookings

down:
	docker-compose down
