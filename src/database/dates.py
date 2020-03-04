import datetime
from src.database.models import Booking

def booked_dates(room):
    bookings = Booking.query.filter_by(room_id = room.id).all()
    booked=[]
    for booking in bookings:
        start = booking.date_in
        end = booking.date_out
        booked += all_dates(start, end)
    return booked


def all_dates(start, end):
    diff = end - start
    dates = [start + datetime.timedelta(days=i) for i in range(diff.days+1)]
    return dates
        
def is_available(room, start_date, end_date):

    potential_dates = all_dates(start_date, end_date)
    dates_booked = booked_dates(room)

    if set(potential_dates).isdisjoint(set(dates_booked)):
        return True
    else:
        return False