import matplotlib.pyplot as pyplot
import math

class Airport:
    # Classe que representa un aeroport amb el seu codi ICAO, coordenades i estat Schengen
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.Schengen = False # Per defecte s'inicialitza com a No-Schengen

def IsSchengenAirport(code):
    # Comprova si un aeroport pertany a l'espai Schengen analitzant el prefix del codi.
    # Retorna True si coincideix amb algun prefix de la llista, sinó False.
    if code == "":
        return False
    llista_codis = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS'
    ]
    prefix = code[0:2]
    trobat = False
    i = 0
    while i < len(llista_codis) and not trobat: #Fem una cerca per trobar els prefixos
        if llista_codis[i] == prefix:
            trobat = True
        else:
            i = i + 1
    return trobat

def SetSchengen(airport):
    # Actualitza l'atribut Schengen de l'objecte Airport passat per paràmetre
    airport.Schengen = IsSchengenAirport(airport.code)

def PrintAirport(airport):
    # Mostra per consola les dades estructurades d'un aeroport.
    print("Code:", airport.code, "Lat:", airport.lat, "Lon:", airport.lon, "Schengen:", airport.Schengen)

def _string_to_decimal(coord_str):
    # Ho utilizem per convertir les coordenades a graus decimals (float)
    direccio = coord_str[0]
    if len(coord_str) == 7:
        d = float(coord_str[1:3]) # Graus
        m = float(coord_str[3:5]) # Minuts
        s = float(coord_str[5:7]) # Segons
    else:
        d = float(coord_str[1:4])
        m = float(coord_str[4:6])
        s = float(coord_str[6:8])

    decimal = d + (m / 60.0) + (s / 3600.0)
    # Si la direcció és Sud o Oest (West), la coordenada decimal ha de ser negativa
    if direccio == 'S' or direccio == 'W':
        decimal = -decimal
    return decimal

def LoadAirports(Airports):
    llista_aeroports = []
    try:
        f = open(Airports, 'r')
        linies = f.readlines()
        f.close()

        n = 1 #Saltem la primera linea que no té informació
        while n < len(linies):
            parts = linies[n].split(" ")
            if len(parts) >= 3:
                codi = parts[0]
                lat_dec = _string_to_decimal(parts[1])
                lon_dec = _string_to_decimal(parts[2])

                nou_ap = Airport(codi, lat_dec, lon_dec)
                llista_aeroports.append(nou_ap)
            n = n + 1

    except FileNotFoundError:
        print("No s'ha trobat el fitxer!")
        return []

    return llista_aeroports

llista = LoadAirports("Airports.txt")

def SaveSchengenAirports(airports, filename):
    # Filtra i guarda en un nou fitxer només aquells aeroports que són Schengen
    if len(airports) == 0:
        return -1

    f = open(filename, 'w')
    f.write("CODE LAT LON\n")
    for a in airports:
        if a.Schengen:
            f.write(a.code + " " + str(a.lat) + " " + str(a.lon) + "\n")
    f.close()


def AddAirport(airports, airport):
    trobat = False
    i = 0
    while i < len(airports) and not trobat:
        if airports[i].code == airport.code:
            trobat = True
        i = i + 1
    if not trobat:
        airports.append(airport)

def RemoveAirport(airports, code):
    i = 0
    while i < len(airports):
        if airports[i].code == code:
            airports.pop(i)
            return
        i = i + 1
    return -1

def PlotAirports(airports):
    s_count = 0
    ns_count = 0
    for a in airports:
        if a.Schengen:
            s_count = s_count + 1
        else:
            ns_count = ns_count + 1

    pyplot.bar(['Airports'], [s_count], color='blue', label='Schengen')
    pyplot.bar(['Airports'], [ns_count], bottom=[s_count], color='red', label='No Schengen')
    pyplot.ylabel('Count')
    pyplot.title('Schengen airports')
    pyplot.legend()
    pyplot.show()


def MapAirports(airports):#hola
    f = open("airports.kml", "w")

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n')
    f.write('<Style id="s_color"><IconStyle><color>ff00ff00</color></IconStyle></Style>\n')
    f.write('<Style id="ns_color"><IconStyle><color>ff0000ff</color></IconStyle></Style>\n')

    for a in airports:
        f.write('<Placemark>\n')
        f.write('<name>' + a.code + '</name>\n')

        if a.Schengen:
            f.write('<styleUrl>#s_color</styleUrl>\n')
        else:
            f.write('<styleUrl>#ns_color</styleUrl>\n')

        f.write('<Point>\n')
        f.write('<coordinates>' + str(a.lon) + ',' + str(a.lat) + '</coordinates>\n')
        f.write('</Point>\n')
        f.write('</Placemark>\n')

    f.write('</Document>\n</kml>')
    f.close()