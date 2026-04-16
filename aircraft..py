import matplotlib.pyplot as pyplot
import math
class Aircraft():
    def __init__(self):
        self.aircraft_id= ""
        self.airline_id= ""
        self.origin_airport= ""
        self.time_of_landing= ""

def LoadArrivals(filename):
    try:
        arrivals = []
        file = open(filename, "r")

        for line in file:
            line = line.strip()

            if line == "":
                continue

            parts = line.split(",")
            if len(parts) != 3:
                continue

            flight = parts[0].strip()
            origin = parts[1].strip()
            time_str = parts[2].strip()

            try:
                hours, minutes = time_str.split(":")
                hours = int(hours)
                minutes = int(minutes)

                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                    continue
            except:
                continue

            aircraft = Aircraft()
            aircraft.flight = flight
            aircraft.origin = origin
            aircraft.scheduled_time = time_str

            arrivals.append(aircraft)

        file.close()

    except FileNotFoundError:
        return []

    return arrivals