import matplotlib.pyplot as pyplot
import math

# Hem creat una classe bàsica per guardar les dades de cada aeroport en un objecte.
# Al mateix constructor cridem a IsSchengenAirport per comprovar el codi al moment de crear-lo.
class Airport:
    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.Schengen = IsSchengenAirport(code)

# Per mirar si és Schengen, tallem les dues primeres lletres del codi (el prefix).
# Hem fet servir un bucle 'while' con un booleà (trobat) perquè si trobem el prefix
# al principi de la llista, el programa s'aturi i així evitem seguir buscant per res.
def IsSchengenAirport(code):
    if code == "":
        return False
    llista_codis = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS'
    ]
    prefix = code[0:2].upper()
    trobat = False
    i = 0
    while i < len(llista_codis) and not trobat:
        if llista_codis[i] == prefix:
            trobat = True
        else:
            i = i + 1
    return trobat

def SetSchengen(airport):
    airport.Schengen = IsSchengenAirport(airport.code)

def PrintAirport(airport):
    print("Code:", airport.code, "Lat:", airport.lat, "Lon:", airport.lon, "Schengen:", airport.Schengen)

# Aquesta funció ens servei per passar el text de coordenades a número decimal.
# Mirem si el text fa 7 caràcters o més (perquè les longituds tenen un dígit més).
# Després apliquem la fórmula de: graus + minuts/60 + segons/3600.
# Si la lletra és Sud (S) o Oest (W), ho multipliquem per -1 perquè quedi negatiu per al mapa.
def _string_to_decimal(coord_str):
    direccio = coord_str[0]
    if len(coord_str) == 7:
        d = float(coord_str[1:3])
        m = float(coord_str[3:5])
        s = float(coord_str[5:7])
    else:
        d = float(coord_str[1:4])
        m = float(coord_str[4:6])
        s = float(coord_str[6:8])

    decimal = d + (m / 60.0) + (s / 3600.0)
    if direccio == 'S' or direccio == 'W':
        decimal = -decimal
    return decimal

# Aquí llegim el fitxer de text línia per línia.
# Hem posat un 'try / except' per si el fitxer no està a la carpeta, així l'aplicació no es penja.
# Fem servir un 'while' que comença a n=1 per saltar-nos la primera línia de capçaleres del text.
# Separem les dades amb '.split()', les passem a decimal i les afegim a la llista.
def LoadAirports(Airports):
    llista_aeroports = []
    try:
        f = open(Airports, 'r')
        linies = f.readlines()
        f.close()

        n = 1
        while n < len(linies):
            linea = linies[n].strip()

            if linea != "":
                parts = linies[n].split()
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

# Filtrem els aeroports de la llista i només els guardem al fitxer si '.Schengen' és True.
# Hem posat un control al principi: si la llista és buida fem un 'return -1' per seguretat.
def SaveSchengenAirports(airports, filename):
    if len(airports) == 0:
        return -1

    f = open(filename, 'w')
    f.write("CODE LAT LON\n")
    for a in airports:
        if a.Schengen:
            f.write(a.code + " " + str(a.lat) + " " + str(a.lon) + "\n")
    f.close()

# Per evitar que s'afegeixin aeroports repetits si es clica molts cops el botó,
# fem un bucle 'while' i comprovem si el codi ja existeix abans de fer l' '.append()'.
def AddAirport(airports, airport):
    trobat = False
    i = 0
    while i < len(airports) and not trobat:
        if airports[i].code == airport.code:
            trobat = True
        i = i + 1
    if not trobat:
        airports.append(airport)

# Busquem l'aeroport que coincideixi amb el codi que ens demanen.
# Si el trobem, l'esborrem amb un '.pop(i)' i sortim directament de la funció amb un 'return'.
# Si el bucle acaba i no ha trobat res, retornarà un -1 d'error.
def RemoveAirport(airports, code):
    i = 0
    while i < len(airports):
        if airports[i].code == code:
            airports.pop(i)
            return
        i = i + 1
    return -1

# Fem un recompte bàsic de quants aeroports són Schengen i quants no amb un bucle 'for'.
# Després fem servir 'pyplot.bar' per dibuixar el gràfic.
# Li hem posat colors verd i vermell per distingir les barres millor.
def PlotAirports(airports):
    s_count = 0
    ns_count = 0
    for a in airports:
        if a.Schengen:
            s_count = s_count + 1
        else:
            ns_count = ns_count + 1

    categorias = ['Schengen', 'Non-Schengen']
    valores = [s_count, ns_count]
    colores = ['green', 'red']

    pyplot.bar(categorias, valores, color=colores)
    pyplot.ylabel('Number of Airports')
    pyplot.title('Schengen vs Non-Schengen Airports')
    pyplot.show()

# Aquí creem el fitxer de Google Earth (.kml) des de zero escrivint el text XML de l'estructura.
# Definim dos estils de xinxetes: 's_color' (verd) i 'ns_color' (vermell).
# Després anem escrivint cada lloc amb un 'for'. A l'etiqueta `<coordinates>` recordem posar
# primer la longitud i després la latitud, que és com ho demana obligatòriament el format KML.
def MapAirports(airports):
    f = open("Files/airports.kml", "w")

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