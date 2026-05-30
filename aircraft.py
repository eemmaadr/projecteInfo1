import math
import matplotlib.pyplot as plt
from airport import LoadAirports, IsSchengenAirport
from tkinter import messagebox

class Aircraft:
    def __init__(self, aircraft_id="", airline="", origin="", scheduled_time="", destination="", departure_time=""):

        self.aircraft_id = aircraft_id              #Info
        self.airline = airline
        self.origin = origin                        #Llegada
        self.scheduled_time = scheduled_time
        self.destination = destination              #Salida
        self.departure_time = departure_time


def LoadArrivals(Arrivals):
    arrivalsList = []
    try:
        with open(Arrivals, "r") as file:
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
                arrivalsList.append(Aircraft(parts[0], parts[3], parts[1], parts[2]))
    except FileNotFoundError:
        print("Archivo no encontrado")
    return arrivalsList

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista esta buida")
        return

    hores_dia = [0] * 24
    i = 0
    while i < len(aircrafts):
        vol = aircrafts[i]
        arrivada = vol.scheduled_time.split(":")
        hora = int(arrivada[0])

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
        actual = aircrafts[i].airline
        found = False
        j = 0
        while j < len(aerolinia) and not found:
            if aerolinia[j] == actual:
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
        llista_schengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
        prefix = vol.origin[0:2]

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

def LoadDepartures(filename):
    departures_list = []
    error = 0
    try:
        file = open(filename, "r")
        next(file)
        for line in file:
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            aircraft_id = parts[0]
            destination = parts[1]
            h, m = parts[2].split(":")
            departure_time = f"{int(h):02d}:{m}"
            airline = parts[3]
            aircraft = Aircraft()
            aircraft.aircraft_id = aircraft_id
            aircraft.destination = destination
            aircraft.departure_time = departure_time
            aircraft.airline = airline
            departures_list.append(aircraft)
        file.close()
    except FileNotFoundError:
        error = -1
    return departures_list, error

def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 or len(departures) == 0:
        return [], -1
    merged = []            # vectores
    departures_used = []
    for arrival in arrivals:     #ponemos clases

        aircraft = Aircraft()
        aircraft.aircraft_id = arrival.aircraft_id
        aircraft.airline = arrival.airline
        aircraft.origin = arrival.origin
        aircraft.scheduled_time = arrival.scheduled_time

        for departure in departures:
            if departure in departures_used:     #si está ocupado pasamos a la siguiente
                continue
            if departure.aircraft_id == arrival.aircraft_id:    #comprovar que es el avión correcto
                arr_h, arr_m = map(int, arrival.scheduled_time.split(":"))
                dep_h, dep_m = map(int, departure.departure_time.split(":"))
                arr_minutes = arr_h * 60 + arr_m     #lo paso aminutos por comodidad
                dep_minutes = dep_h * 60 + dep_m
                if arr_minutes < dep_minutes:    #Comprobar que la llegada es antes que la salida
                    aircraft.destination = departure.destination
                    aircraft.departure_time = departure.departure_time
                    departures_used.append(departure)
                    break   #no hace falta seguir
        merged.append(aircraft)

    for departure in departures:    # la parte de los de noche

        if departure not in departures_used:
            merged.append(departure)

    return merged, 0

def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return [], -1
    night = []                  #creamos el vector de vuelos noche
    for aircraft in aircrafts:
        if aircraft.destination != "" and aircraft.origin == "":    #si no tiene destino o no tiene llegada lo mete, ya que tiene que estar ahí
            night.append(aircraft)          #es un append, añadir al final del vector
    return night, 0                         #devuelve el vector


def TimeToMinutes(time_str):

    if not time_str or time_str == "-" or time_str == "00:00" or time_str == 0:
        return 0
    try:
        parts = time_str.split(':')
        #  assegurem que tenim hores i minuts [1]
        return int(parts[0]) * 60 + int(parts[1])
    except (ValueError, IndexError):
        return 0


def PlotAverageStayTime(aircrafts):

    if not aircrafts:
        messagebox.showerror("Error", "No hi ha dades de vols per generar estadístiques.")
        return

    stats = {}

    for ac in aircrafts:
        if hasattr(ac, 'scheduled_time') and hasattr(ac, 'departure_time'):
            if ac.scheduled_time != "-" and ac.departure_time != "-":
                t_arribada = TimeToMinutes(ac.scheduled_time)
                t_sortida = TimeToMinutes(ac.departure_time)
                if t_sortida < t_arribada: # CÀLCUL AMB CANVI DE DIA:
                    t_sortida += 24 * 60
                durada = t_sortida - t_arribada
                # FILTRE
                if 30 < durada < 700:
                    if ac.airline not in stats:
                        stats[ac.airline] = [0, 0]  # [suma_minuts, comptador]
                    stats[ac.airline][0] += durada
                    stats[ac.airline][1] += 1

    # Preparació dades
    if not stats:
        messagebox.showwarning("Atenció", "No s'han trobat vols amb dades compatibles.")
        return

    aerolinies = list(stats.keys())
    mitjanes = [val[0] / val[1] for val in stats.values()]

    # Visualització
    plt.figure(figsize=(10, 6))
    plt.bar(aerolinies, mitjanes, color='orange', edgecolor='black')
    plt.title("Temps d'Estada Mitjà per Aerolínia (Minuts)")
    plt.xlabel("Codi ICAO")
    plt.ylabel("Temps mitjà")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":

    lista = LoadArrivals("Arrivals.txt")
    if lista:
        print(f"Test exitoso: {len(lista)} vuelos cargados.")
        PlotArrivals(lista)