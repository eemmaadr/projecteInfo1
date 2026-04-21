import math
import matplotlib.pyplot as plt
from airport import LoadAirports, IsSchengenAirport


class Aircraft:
    def __init__(self, aircraft_id="", airline="", origin="", scheduled_time=""):

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

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista esta buida")
        return

    hores_dia = [0] * 24
    i = 0
    while i < len(aircrafts):
        vol = aircrafts[i]
        arrivada = vol.scheduled_time.split(":")
        hora = int(arrivada)

        if 0 <= hora < 24:
            hores_dia[hora] += 1
        i += 1

    X = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
    plt.bar(X, hores_dia, color='skyblue')
    plt.ylabel("Nombre de vols")
    plt.xlabel("Hora del dia")
    plt.title("Freqüència d'aterratges a Barcelona (LEBL)")
    plt.show()

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista de vols està buida.")
        return

    aerolinia = []
    vols = []
    i = 0
    while i < len(aircrafts):
        actual = aircrafts[i].aircraft_id
        found = False
        j = 0
        while j < len(aerolinia) and not found:
            if aerolinia == actual:
                vols[j] += 1
                found = True
            j += 1
        if not found:
            aerolinia.append(actual)
            vols.append(1)
        i += 1

    plt.bar(aerolinia, vols, color='orange')
    plt.xlabel("Aerolínia")
    plt.ylabel("Nombre de vols")
    plt.title("Vols per companyia aèria")
    plt.show()

def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista de vols està buida")
        return

    Schengen = 0
    NoSchengen = 0
    i = 0
    while i < len(aircrafts):
        vol = aircrafts[i]
        codi_origen = vol.origin
        llista_schengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
        prefix = codi_origen[0:2]

        es_schengen = False
        j = 0
        while j < len(llista_schengen):
            if llista_schengen[j] == prefix:
                es_schengen = True
                j += 1

            if es_schengen:
                Schengen += 1

            else:
                NoSchengen += 1
            i += 1

    categories = ['Schengen', 'No Schengen']
    valors = [Schengen, NoSchengen]
    plt.bar(categories, valors)
    plt.ylabel("Nombre de vols")
    plt.title("Arribades Schengen vs No-Schengen a LEBL")
    plt.legend()
    plt.show()

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