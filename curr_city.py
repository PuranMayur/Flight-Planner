class CurrentCity:
    def __init__(self, city, arrived_flight, prev_city):
        self.city = city
        self.arrived_flight = arrived_flight
        self.prev_city = prev_city
        self.total_fare = (prev_city.total_fare if prev_city is not None else 0) + (arrived_flight.fare if arrived_flight is not None else 0)
        self.total_flights = (prev_city.total_flights if prev_city is not None else 0) + (1 if arrived_flight is not None else 0)
        
    def __str__(self):
        return f"city {self.city}"
    
    def __repr__(self):
        return self.__str__()
