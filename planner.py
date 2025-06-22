from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        
        self.flights = flights
        self.city_no = 0
        for flight in flights:
            self.city_no = max(self.city_no, flight.start_city, flight.end_city)
        self.adjacency_list = [[] for _ in range(self.city_no+1)]
        for flight in flights:
            self.adjacency_list[flight.start_city].append(flight)
        pass
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        if start_city == end_city:
            return []

        city_queue = Queue()
        city_queue.enqueue(CurrentCity(start_city, None, None))
        possible_routes = []
        vis_flights = [False] * (len(self.flights)+1)
        min_dist = float('inf')

        while not city_queue.is_empty():
            current_city = city_queue.dequeue()

            if current_city.total_flights > min_dist:
                break

            if current_city.city == end_city:
                if min_dist == float('inf'):
                    min_dist = current_city.total_flights
                if current_city.total_flights == min_dist:
                    possible_routes.append(current_city)
                    continue           

            for flight in self.adjacency_list[current_city.city]:
                if flight.departure_time >= 20 + (current_city.arrived_flight.arrival_time if current_city.arrived_flight is not None else (t1 - 20)) and flight.departure_time >= t1 and flight.arrival_time <= t2 and not vis_flights[flight.flight_no]:
                        
                    vis_flights[flight.flight_no] = True
                    city_queue.enqueue(CurrentCity(flight.end_city, flight, current_city))

        if len(possible_routes) == 0:
            return []

        best_route = min(possible_routes, key=lambda x: (x.total_flights, x.arrived_flight.arrival_time if x.arrived_flight else t1))

        route = []
        while best_route.prev_city is not None:
            route.append(best_route.arrived_flight)
            best_route = best_route.prev_city
        return route[::-1]
        pass
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        
        if start_city == end_city:
            return []
        
        pq = Heap(init_array=[((CurrentCity(start_city, None, None)), 0)], comparison_function=lambda x, y: x[1] <= y[1])
        vis_flights = [False for _ in range(len(self.flights)+1)]
        
        while pq.top() is not None:
            current_city = pq.extract()[0]
            # current_city.total_fare += current_city.arrived_flight.fare if current_city.arrived_flight is not None else 0
            
            if current_city.city == end_city:
                route = []
                while current_city.prev_city is not None:
                    route.append(current_city.arrived_flight)
                    current_city = current_city.prev_city
                return route[::-1]
            
            for flight in self.adjacency_list[current_city.city]:
                if flight.departure_time >= 20 + (current_city.arrived_flight.arrival_time if current_city.arrived_flight is not None else (t1-20)) and flight.departure_time >= t1 and flight.arrival_time <= t2 and not vis_flights[flight.flight_no]:
                    vis_flights[flight.flight_no] = True
                    pq.insert(((CurrentCity(flight.end_city, flight, current_city)), current_city.total_fare + flight.fare))
        return []
        pass
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        
        if start_city == end_city:
            return []
        
        pq = Heap(init_array=[((CurrentCity(start_city, None, None)), 0, 0)], comparison_function=lambda x, y: (x[1] < y[1]) or (x[1] == y[1] and x[2] <= y[2]))
        vis_flights = [False for _ in range(len(self.flights)+1)]
        
        while pq.top() is not None:
            current_city = pq.extract()[0]
            
            if current_city.city == end_city:
                route = []
                while current_city.prev_city is not None:
                    route.append(current_city.arrived_flight)
                    current_city = current_city.prev_city
                return route[::-1]
            
            for flight in self.adjacency_list[current_city.city]:
                if flight.departure_time >= 20 + (current_city.arrived_flight.arrival_time if current_city.arrived_flight is not None else (t1-20)) and flight.departure_time >= t1 and flight.arrival_time <= t2 and not vis_flights[flight.flight_no]:
                        vis_flights[flight.flight_no] = True
                        pq.insert(((CurrentCity(flight.end_city, flight, current_city)), current_city.total_flights + 1, current_city.total_fare + flight.fare))
        return []
        pass

# All utility classes are below

# 1 Queuezz
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)
        
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
        
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        
        data = self.front.data
        self.front = self.front.next
        
        if self.front is not None:
            self.front.prev = None
        else:
            self.rear = None
        
        self.size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self.front.data

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size
    
# 2 CurrentCityNode
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

# 3 Heap
class Heap:
    
    def __init__(self, comparison_function, init_array):
        self.comparison_function = comparison_function
        self.heap = init_array
        self.build_heap()
        pass
    
    def build_heap(self):
        
        for i in range(len(self.heap) // 2, -1, -1):
            self._heapify_down(i)
    
    def _heapify_up(self, index):
        
        parent_index = (index - 1) // 2
        if index > 0 and not self.comparison_function(self.heap[parent_index], self.heap[index]):
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        smallest = index

        if left_child < len(self.heap) and not self.comparison_function(self.heap[smallest], self.heap[left_child]):
            smallest = left_child
        if right_child < len(self.heap) and not self.comparison_function(self.heap[smallest], self.heap[right_child]):
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
    
    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
        pass
    
    def extract(self):
        if len(self.heap) == 0:
            return None

        top_value = self.heap[0]
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        self.heap[0] = self.heap.pop()
        if self.heap:
            self._heapify_down(0)
        
        return top_value
        pass
    
    def top(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0]
        pass
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def __str__(self):
        return str(self.heap)
    
    def __repr__(self):
        return self.__str__()
