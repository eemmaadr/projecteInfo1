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

def SaveFlights(aircrafts, filename):
    if not aircrafts:
        print("Error: lista vacía")
        return -1

    file = open(filename, "w")

    for a in aircrafts:
        aircraft_id = a.aircraft_id if a.aircraft_id != "" else "-"
        origin = a.origin_airport if a.origin_airport != "" else "-"
        time = a.time_of_landing if a.time_of_landing != "" else "-"
        airline = a.airline_id if a.airline_id != "" else "-"

        line = f"{aircraft_id} {origin} {time} {airline}\n"
        file.write(line)

    file.close()
    return 0


def MapFlights(aircrafts):
    if not aircrafts:
        print("Error: lista vacía")
        return

    airports = LoadAirports("Airports.txt")

    if "LEBL" not in airports:
        print("Error: LEBL no encontrado")
        return

    lebl = airports["LEBL"]

    file = open("flights.kml", "w")

    file.write("""<?xml version="1.0" encoding="UTF-8"?> <kml xmlns="http://www.opengis.net/kml/2.2"> <Document>""")

    for a in aircrafts:
        if a.origin_airport not in airports:
            continue

        origin = airports[a.origin_airport]

        file.write(f""" <Placemark> <name>{a.aircraft_id}</name> <LineString> <coordinates> {origin[1]},{origin[0]},0 {lebl[1]},{lebl[0]},0 </coordinates> </LineString> </Placemark> """)

    file.write("""
</Document>
</kml>
""")

    file.close()

    print("Archivo flights.kml generado ")
