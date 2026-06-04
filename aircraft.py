import math
import matplotlib.pyplot as plt
from airport import LoadAirports, IsSchengenAirport
from tkinter import messagebox

# Hem creat la classe Aircraft amb tots els paràmetres buits per defecte.
# D'aquesta manera, ens serveix tant per guardar un vol que només té arribada,
# un que només té sortida, o un moviment complet fusionat.
class Aircraft:
    def __init__(self, aircraft_id="", airline="", origin="", scheduled_time="", destination="", departure_time=""):

        self.aircraft_id = aircraft_id              #Info
        self.airline = airline
        self.origin = origin                        #Llegada
        self.scheduled_time = scheduled_time
        self.destination = destination              #Salida
        self.departure_time = departure_time

# Aquí llegim el fitxer d'arribades (Arrivals). Fem una neteja de cadenes i comprovem
# que cada línia tingui exactament 4 trossos. També mirem que l'hora estigui en format correcte
# (entre 0 i 23 per a les hores, i 0 i 59 per als minuts) abans de guardar l'objecte a la llista.
def LoadArrivals(Arrivals):
    arrivalsList = []
    try:
        f = open(Arrivals, "r")
        linies = f.readlines()
        f.close()

        n = 1
        while n < len(linies):
            linea = linies[n].strip()
            if linea != "":
                parts = linea.split()
                if len(parts) == 4:
                    time_str = parts[2]
                    if ":" in time_str:
                        time_parts = time_str.split(':')
                        h = int(time_parts[0])
                        m = int(time_parts[1])
                        if 0 <= h <= 23 and 0 <= m <= 59:
                            nou_vuelo = Aircraft(parts[0], parts[3], parts[1], parts[2])
                            arrivalsList.append(nou_vuelo)
            n += 1
    except FileNotFoundError:
        print("Archivo no encontrado")
    return arrivalsList

# Per fer aquest gràfic, hem creat una llista de 24 posicions plenes de zeros (hores_dia).
# Anem recorrent els vols, extraiem l'hora de l'arribada fent un '.split(":")' i sumem +1
# a la posició de la llista que correspongui a aquella hora. Després ho pintem tot amb barres blaves.
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

# Aquí anem acumulant quantes vegades surt cada aerolínia. Com que no sabem quines companyies hi ha,
# si l'aerolínia no s'havia vist abans (found == False), l'afegim a la llista d'aerolínies i posem el seu
# comptador a 1. Si ja existia, només sumem 1 al seu índex.
# NOTA EXTRA: Hem configurat la rotació a 90º i 'tight_layout' perquè els codis es puguin llegir bé.
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista de vols està buida.")
        return

    aerolinia = []
    vols = []
    i = 0
    while i < len(aircrafts):
        actual = aircrafts[i].airline
        if actual != "":
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

    plt.figure(figsize=(12, 6))
    plt.bar(aerolinia, vols, color='orange')
    plt.xlabel("Aerolínia")
    plt.ylabel("Nombre de vols")
    plt.title("Vols per companyia aèria")
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    plt.show()

# Cridem a la funció del mòdul anterior 'IsSchengenAirport' passant l'origen del vol.
# Així anem sumant als comptadors de Schengen o No-Schengen per dibuixar les dues barres comparatives.
def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error: La llista de vols està buida")
        return

    Schengen = 0
    NoSchengen = 0
    i = 0
    while i < len(aircrafts):
        vol = aircrafts[i]
        if vol.origin != "":
            if IsSchengenAirport(vol.origin):
                Schengen += 1
            else:
                NoSchengen += 1
        i += 1

    categories = ['Schengen', 'No Schengen']
    valors = [Schengen, NoSchengen]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, valors, color=['green', 'red'], edgecolor='black')
    plt.ylabel("Nombre de vols")
    plt.title("Arribades Schengen vs No-Schengen a LEBL")
    plt.tight_layout()
    plt.show()

# Funció simple per guardar la llista de vols a un fitxer de text.
# Si algun paràmetre de l'objecte està completament buit, escrivim dues cometes simples ''
# per mantenir les columnes ben quadrades i que el fitxer no es deformi.
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

# Aquí calculem la distància en línia recta entre dues coordenades del planeta (en km).
# Passem primer els graus a radiants amb 'math.radians' i després apliquem la fórmula matemàtica.
def Haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Busquem primer on està l'aeroport de Barcelona (LEBL) a la llista d'aeroports.
# Després mirem d'on ve cada vol, calculem la distància amb la funció Haversine i,
# si el resultat és superior a 2000 km, el guardem com un vol de llarga distància.
def LongDistanceArrivals(aircrafts):
    airports_list = LoadAirports("Airports.txt")
    res = []

    lebl = None
    i = 0
    while i < len(airports_list):
        if airports_list[i].code == "LEBL":
            lebl = airports_list[i]
        i += 1

    if lebl is None:
        return res

    for a in aircrafts:
        orig_ap = None
        j = 0
        while j < len(airports_list):
            if airports_list[j].code == a.origin:
                orig_ap = airports_list[j]
            j += 1

        if orig_ap is not None:
            if Haversine(orig_ap.lat, orig_ap.lon, lebl.lat, lebl.lon) > 2000:
                res.append(a)
    return res

# Generem un KML de línies de vol que van des de l'origen fins a Barcelona (LEBL).
# Per agafar ràpidament les coordenades dels aeroports d'origen hem fet servir un diccionari,
# que ens estalvia haver de recórrer tota la llista d'aeroports amb un bucle a cada vol.
# Si el vol prové de Schengen pintem la línia verda, i si ve de fora la pintem vermella.
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

# Llegim el fitxer de sortides (Departures) per a la Versió 4.
# Fem servir el truc de posar 'next(file)' per saltar-nos automàticament la primera línia de títols.
# Guardem l'hora amb el format quadrat de dos dígits usant un format de text f-string (f"{int(h):02d}:{m}").
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

# Aquí ajuntem els moviments d'arribada i sortida. Recorrem les arribades i busquem si el mateix
# avió té una sortida programada més tard (convertint les hores a minuts totals).
# Si té sentit, ajuntem origen i destí al mateix objecte i guardem aquella sortida a 'departures_used'
# perquè cap altre avió la pugui agafar. Al final del tot, els vols de sortida que hagin quedat sols
# s'afegeixen directament com a vols independents.
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
                if ":" in arrival.scheduled_time and ":" in departure.departure_time:
                    arr_minutes = TimeToMinutes(arrival.scheduled_time)
                    dep_minutes = TimeToMinutes(departure.departure_time)

                    if arr_minutes < dep_minutes:
                        aircraft.destination = departure.destination
                        aircraft.departure_time = departure.departure_time
                        departures_used.append(departure)
                        break  #no hace falta seguir
        merged.append(aircraft)

    for departure in departures:    # la parte de los de noche

        if departure not in departures_used:
            merged.append(departure)

    return merged, 0

# Filtrem quins avions dormen a l'aeroport (avions de nit). Són aquells que tenen una sortida assignada
# (destination) però que, en canvi, no s'ha registrat cap arribada prèvia des de la base de dades (origin buit).
def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return [], -1
    night = []                  #creamos el vector de vuelos noche
    for aircraft in aircrafts:
        if aircraft.destination != "" and aircraft.origin == "":    #si no tiene destino o no tiene llegada lo mete, ya que tiene que estar ahí
            night.append(aircraft)          #es un append, añadir al final del vector
    return night, 0                         #devuelve el vector

# Funció auxiliar molt pràctica: passa una cadena tipus "HH:MM" a minuts totals de l'estil enters
# (Multiplicant hores * 60 + minuts) per poder fer restes i comparacions de temps fàcilment.
def TimeToMinutes(time_str):

    if not time_str or time_str == "-" or time_str == "00:00" or time_str == 0:
        return 0
    try:
        parts = time_str.split(':')
        #  assegurem que tenim hores i minuts [1]
        return int(parts[0]) * 60 + int(parts[1])
    except (ValueError, IndexError):
        return 0

# PLOT EXTRA: Calculem el temps mitjà que passa un avió a terra per cada companyia.
# Si l'hora de sortida és menor que la d'arribada significa que ha passat la nit de canvi de dia,
# així que sumem 24 hores en minuts (24 * 60) per evitar restes negatives errònies. Comprovar si es atribut
# També filtrem temps absurds (menys de 30 minuts o més de 700 minuts) per netejar les dades corruptes.
def PlotAverageStayTime(aircrafts):

    if not aircrafts:
        messagebox.showerror("Error", "No hi ha dades de vols per generar estadístiques.")
        return

    aerolinies = []
    suma_minuts = []
    comptador_vols = []

    for ac in aircrafts:

            if ac.scheduled_time != "-" and ac.departure_time != "-":
                t_arribada = TimeToMinutes(ac.scheduled_time)
                t_sortida = TimeToMinutes(ac.departure_time)

                if t_sortida < t_arribada: # CÀLCUL AMB CANVI DE DIA:
                    t_sortida += 24 * 60
                durada = t_sortida - t_arribada

                # FILTRE
                if 30 < durada < 700:
                    found = False
                    idx = 0
                    while idx < len(aerolinies) and not found:
                        if aerolinies[idx] == ac.airline:
                            suma_minuts[idx] += durada
                            comptador_vols[idx] += 1
                            found = True
                        idx += 1

                    if not found:
                        aerolinies.append(ac.airline)
                        suma_minuts.append(durada)
                        comptador_vols.append(1)

    if len(aerolinies) == 0:
        messagebox.showwarning("Atenció", "No s'han trobat vols amb dades compatibles.")
        return

        # Calcular las medias
    mitjanes = []
    for k in range(len(aerolinies)):
        mitjanes.append(suma_minuts[k] / comptador_vols[k])

    # Visualització
    plt.figure(figsize=(14, 6))
    plt.bar(aerolinies, mitjanes, color='orange', edgecolor='black')
    plt.title("Temps d'Estada Mitjà per Aerolínia (Minuts)")
    plt.xlabel("Codi ICAO")
    plt.ylabel("Temps mitjà")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=90, fontsize=7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pass