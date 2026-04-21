import math
import matplotlib.pyplot as plt
from airport import LoadAirports, IsSchengenAirport


class Aircraft:
    def __init__(self, aircraft_id="", airline="", origin="", scheduled_time=""):
        # Atributos exactos según el PDF
        self.aircraft_id = aircraft_id
        self.airline = airline
        self.origin = origin
        self.scheduled_time = scheduled_time


def LoadArrivals(filename):
    arrivals = []
    try:
        with open(filename, "r") as file:
            next(file)
            for line in file:
                parts = line.strip().split()
                if len(parts) != 4: continue


                time_str = parts[2]
                try:
                    h, m = map(int, time_str.split(':'))
                    if not (0 <= h <= 23 and 0 <= m <= 59): continue
                except:
                    continue

                arrivals.append(Aircraft(parts[0], parts[3], parts[1], parts[2]))
    except FileNotFoundError:
        print("Archivo no encontrado")
    return arrivals


def SaveFlights(aircrafts, filename):
    if not aircrafts: return -1
    try:
        with open(filename, "w") as file:
            file.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
            for a in aircrafts:
                aid = a.aircraft_id if a.aircraft_id else "''"
                ori = a.origin if a.origin else "''"
                tim = a.scheduled_time if a.scheduled_time else "''"
                air = a.airline if a.airline else "''"
                file.write(f"{aid} {ori} {tim} {air}\n")
        return 0
    except:
        return -1


def Haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def LongDistanceArrivals(aircrafts):
    airports_list = LoadAirports("Airports.txt")
    airports_dict = {a.code: a for a in airports_list}
    lebl = airports_dict.get("LEBL")
    res = []
    if not lebl: return res
    for a in aircrafts:
        if a.origin in airports_dict:
            ori = airports_dict[a.origin]
            if Haversine(ori.lat, ori.lon, lebl.lat, lebl.lon) > 2000:
                res.append(a)
    return res


def PlotArrivals(aircrafts):
    horas = [int(a.scheduled_time.split(':')[0]) for a in aircrafts]
    plt.figure("Histograma de Llegadas")
    plt.hist(horas, bins=range(25), edgecolor='black', color='skyblue')
    plt.title("Vuelos llegados por franja horaria")
    plt.xlabel("Hora del día")
    plt.ylabel("Cantidad de vuelos")
    plt.show()


def PlotAirlines(aircrafts):
    counts = {}
    for a in aircrafts:
        counts[a.airline] = counts.get(a.airline, 0) + 1
    plt.figure("Vuelos por Aerolínea")
    plt.bar(counts.keys(), counts.values(), color='orange')
    plt.title("Distribución por Compañía")
    plt.show()


def PlotFlightsType(aircrafts):
    sch = sum(1 for a in aircrafts if IsSchengenAirport(a.origin))
    no_sch = len(aircrafts) - sch
    plt.figure("Schengen vs No-Schengen")
    plt.bar(['Vuelos'], [sch], label='Schengen', color='green')
    plt.bar(['Vuelos'], [no_sch], bottom=[sch], label='No-Schengen', color='red')
    plt.title("Tipo de procedencia (Apilado)")
    plt.legend()
    plt.show()


def MapFlights(aircrafts, filename):
    airports_list = LoadAirports("Airports.txt")
    airports_dict = {a.code: a for a in airports_list}
    lebl = airports_dict.get("LEBL")
    if not lebl: return

    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n')
        for a in aircrafts:
            if a.origin in airports_dict:
                ori = airports_dict[a.origin]
                color = "ff00ff00" if IsSchengenAirport(a.origin) else "ff0000ff"
                f.write(
                    f'<Placemark><name>{a.aircraft_id}</name><Style><LineStyle><color>{color}</color><width>2</width></LineStyle></Style>')
                f.write(
                    f'<LineString><coordinates>{ori.lon},{ori.lat},0 {lebl.lon},{lebl.lat},0</coordinates></LineString></Placemark>\n')
        f.write('</Document></kml>')


if __name__ == "__main__":

    lista = LoadArrivals("Arrivals.txt")
    if lista:
        print(f"Test exitoso: {len(lista)} vuelos cargados.")
        PlotArrivals(lista)