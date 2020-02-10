postgres_config:
	docker-compose up -d
	psql hotel_bookings <  hotel_data.psql -U postgres -h localhost -p 5433
	
flask:
	python3 app.py

psql:
	psql postgresql://postgres:hotel@localhost:5433/hotel_bookings


