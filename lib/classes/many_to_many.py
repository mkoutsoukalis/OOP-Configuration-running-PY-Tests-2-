
class NationalPark:

    def __init__(self, name):
        self.name = name
        self.visitor_list = []
        self.trip_list = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if hasattr(self, "_name"):
            raise Exception("Name of the national park cannot be modified after creation.")
        if not isinstance(name, str):
            raise TypeError("Name should be a string")
        if len(name) < 3:
            raise ValueError("Name should have at least 3 characters")
        self._name = name
        
    def trips(self, new_trip=None):
        from classes.many_to_many import Trip
        if new_trip is not None and isinstance(new_trip, Trip):
            self.trip_list.append(new_trip)
        return self.trip_list or []
    
    def visitors(self, visitor=None):
        from classes.many_to_many import Visitor
        visitor_unique = (visitor not in self.visitor_list)
        visitor_valid = isinstance(visitor, Visitor)
        if visitor_unique and visitor_valid:
            self.visitor_list.append(visitor)
        return self.visitor_list or []
        
 
    def total_visits(self):
        return len(self.trips())
        
    
    def best_visitor(self):
        from collections import Counter
        trip_visitors = [trip.visitor for trip in self.trips()]
        visitor_counts = Counter(trip_visitors)
        best_visitor, _ = visitor_counts.most_common(1)[0]
        return best_visitor


class Trip:
    all = []
    def __init__(self, visitor, national_park, start_date, end_date):
        self.visitor = visitor
        self.national_park = national_park
        self.start_date = start_date
        self.end_date = end_date

        Trip.all.append(self)

        self.national_park.visitors(self.visitor)
        visitor.trips(self)
        national_park.trips(self)
        
        visitor.national_parks(national_park)
        

    @property
    def start_date(self):
        return self._start_date
    
    @start_date.setter
    def start_date(self, start_date):
        import re
        if not isinstance(start_date, str):
            raise Exception("start_date should be a string")
        start_date_charc_limit = (len(start_date) >= 7)
        start_date_format = re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2})(st|nd|rd|th)$', start_date)
        if start_date_charc_limit and start_date_format:
            self._start_date = start_date
        else:
            raise Exception("Invalid start date format")
        
    @property
    def end_date(self):
        return self._end_date
    
    @end_date.setter
    def end_date(self, end_date):
        import re
        if not isinstance(end_date, str):
            raise Exception ("not a string")
        end_date_charc_limit = (len(end_date) >= 7)
        end_date_format = re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2})(st|nd|rd|th)$', end_date)
        if end_date_charc_limit and end_date_format:
            self._end_date = end_date
        if not end_date_format:
            raise Exception("Invalid end date format")

class Visitor:

    def __init__(self, name):
        self.name = name
        self.trip_list = []
        self.park_list = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name should be a string")
        if not (1 <= len(name) <= 15):
            raise ValueError("Name should be between 1 and 15 characters long")
        self._name = name
            
    def trips(self, new_trip=None):
        trip_already_exists = (new_trip is not None) 
        trip_valid = isinstance(new_trip, Trip)
        if trip_already_exists and trip_valid:
            self.trip_list.append(new_trip)
        return self.trip_list
    
    def national_parks(self, park=None):
        if park is not None and isinstance(park, NationalPark) and park not in self.park_list:
            self.park_list.append(park)
        return self.park_list
    
    def total_visits_at_park(self, park):
        visit_count = 0
        for trip in self.trip_list:
            if trip.national_park == park:
                visit_count += 1
            return visit_count