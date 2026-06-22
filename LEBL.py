import matplotlib.pyplot as pyplot
import math
import os

from airport import IsSchengenAirport
# Definim les quatre classes que ens organitzen l'estructura de l'aeroport per nivells:
# L'aeroport conté terminals, les terminals contenen àrees d'embarcament (amb les seves companyies),
# i les àrees contenen les portes d'embarcament (gates).
class BarcelonaAp:
    def __init__(self,code):
        self.code = code
        self.terminals= []
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boardingareas = []
        self.airlines=[]
class BoardingArea:
    def __init__(self,name,type):
        self.name = name
        self.type = type
        self.gates=[]
class Gate:
    def __init__(self,name):
        self.name = name
        self.ocupat= False
        self.id="-"

# Busquem el fitxer corresponent a cada terminal (ex: T1_Airlines.txt).
# Anem llegint el fitxer línia per línia separant per tabuladors ("\t") per extreure
# el codi ICAO de cada companyia i guardar-lo a la llista d'aerolínies de la terminal.
def LoadAirlines(terminal, t_name):

    filename = t_name + "_Airlines.txt"     #construimos nombre de archivo con las T

    if not os.path.exists(filename):
        return -1

    airlines_list = []

    with open(filename, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if line != "":

                parts = line.split("\t")    #divide,

                if len(parts) >= 2:

                    airline_code = parts[1]

                    airlines_list.append(airline_code)   #Añade aerolinia a la lista

    terminal.airlines = airlines_list

    return 0

# Aquesta funció llegeix la configuració de l'aeroport (Terminals.txt).
# Primer agafem el codi de l'aeroport i el nombre de terminals totals. Després, amb bucles aniuats,
# anem llegint cada terminal, creem les seves àrees d'embarcament i en generem les portes
# cridant a 'SetGates'. Al final ens retorna tot l'arbre d'objectes connectat.
def LoadAirportStructure(filename):

    if not os.path.exists(filename):
        return -1

    with open(filename, "r", encoding="utf-8") as file:

        first_line = file.readline().strip().split()

        airport_code = first_line[0]    #Guarda el código y el número

        num_terminals = int(first_line[1])

        bcn = BarcelonaAp(airport_code)   #Crea el aeropuerto

        for i in range(num_terminals):   #Repite tantas veces como terminales haya.

            terminal_line = file.readline().strip().split()

            terminal_name = terminal_line[1]

            num_areas = int(terminal_line[2])

            terminal = Terminal(terminal_name)   #Crea la terminal

            LoadAirlines(terminal, terminal_name)

            for j in range(num_areas):

                area_line = file.readline().strip().split()

                area_name = area_line[1]

                area_type = area_line[2]

                init_gate = int(area_line[4])

                end_gate = int(area_line[6])

                area = BoardingArea(area_name, area_type)    #Crea boarding area.

                prefix = terminal_name + "BA" + area_name + "G"

                SetGates(area, init_gate, end_gate, prefix)   #Crea las puertas

                terminal.boardingareas.append(area)   #Añade el área al terminal

            bcn.terminals.append(terminal)   #Añade terminal al aeropuerto

    return bcn    #Te da el aeropurto completo

# Recorrem les terminals de l'aeroport per buscar quina d'elles opera la companyia que ens demanen.
# Fem servir la funció auxiliar 'IsAirlineInTerminal' per comprovar la llista.
def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:    #Recorre terminales
        if IsAirlineInTerminal(terminal, name):    #comprueba
            return terminal.name  #si la encuentra retorna la terminal

    return ""

# Assignem una porta lliure a un avió basant-nos en dues regles obligatòries:
# 1. Que estigui a la terminal assignada a la seva companyia aèria.
# 2. Que el tipus d'àrea coincideixi amb l'origen (Schengen o non-Schengen).
# Si trobem una porta buida, la marquem com a ocupada i hi guardem l'ID de l'avió.
def AssignGate(bcn, aircraft):

    terminal_name = SearchTerminal(bcn, aircraft.airline)   #Busca terminal de la aerolínea
    if terminal_name == "":
        return -1
    if IsSchengenAirport(aircraft.origin):
        required_type = "Schengen"
    else:
        required_type = "non-Schengen"     #schengen
    for terminal in bcn.terminals:   #Recorre terminales

        if terminal.name == terminal_name:    #Recorre áreas

            for area in terminal.boardingareas:

                if area.type == required_type:

                    for gate in area.gates:         #Recorre puertas

                        if gate.ocupat == False:
                            gate.ocupat = True
                            gate.id = aircraft.aircraft_id
                            gate.origin = aircraft.origin

                            return 0

    return -1

# Generem de manera seqüencial totes les portes d'una àrea des de la porta inicial fins a la final.
# Els hi donem el nom combinant el prefix de la zona amb el número actual (ex: T1BAAG1).
def SetGates(area, init_gate, end_gate, prefix):
    if end_gate<= init_gate:
        return -1
    area.gates=[]
    for i in range(init_gate, end_gate+1):
        nomporta= prefix + str(i)
        novaporta= Gate(nomporta)
        area.gates.append(novaporta)

        novaporta.ocupat = False
        novaporta.id="-"

    return 0

def IsAirlineInTerminal(terminal, name):

    if name == "" or name is None:
        return False

    if not terminal.airlines:
         return False
    return name in terminal.airlines

# Recorrem absolutament totes les portes de l'aeroport amb bucles 'while' aniuats
# per extreure una llista simple de l'estat de cadascuna (nom, si està ocupada i quin avió hi ha).
def GateOccupancy(bcn):
    llista_estat = []
    i = 0
    while i < len(bcn.terminals):
        t = bcn.terminals[i]
        j = 0
        while j < len(t.boardingareas):
            ba = t.boardingareas[j]
            k = 0
            while k < len(ba.gates):
                g = ba.gates[k]
                llista_estat.append([g.name, g.ocupat, g.id])
                k += 1
            j += 1
        i += 1
    return llista_estat

# Aquesta funció dibuixa un plànol gràfic de l'aeroport amb matplotlib.
# Hem col·locat les àrees i els passadissos calculant coordenades X i Y perquè quedin separats.
# Pintem quadradets de color vermell si la porta està ocupada (afegint l'ID de l'avió) i verds si està lliure.
def PlotGateOccupancy(bcn):
    if not bcn or not bcn.terminals:
        print("Error: No hi ha dades de l'aeroport.")
        return

    fig, ax = pyplot.subplots(figsize=(25, 11))

    pos_ba_X = 2
    y_minima_detectada = -26

    for t in bcn.terminals:
        y_base = 0 if "1" in t.name else -15

        largo_barra = len(t.boardingareas) * 15.5

        ax.plot([pos_ba_X - 2, pos_ba_X + largo_barra - 4], [y_base, y_base],
                color='blue', linewidth=6, solid_capstyle='butt')

        ax.text(pos_ba_X - 2.5, y_base, t.name, fontsize=14, weight='bold', verticalalignment='center')

        for ba in t.boardingareas:
            letra_zona = ba.name.replace("Area ", "").upper()
            if not letra_zona:
                letra_zona = ba.name

            max_puertas = len(ba.gates)
            largo_pasillo = max(7, (max_puertas // 2) * 1.3)

            punto_final_pasillo = y_base - largo_pasillo
            if punto_final_pasillo < y_minima_detectada:
                y_minima_detectada = punto_final_pasillo

            ax.plot([pos_ba_X, pos_ba_X], [y_base, punto_final_pasillo], color='blue', linewidth=6,
                    solid_capstyle='butt')
            ax.text(pos_ba_X, punto_final_pasillo - 0.8, letra_zona, fontsize=12, weight='bold',
                    horizontalalignment='center')

            pos_g_Y = y_base - 1.0

            for index, g in enumerate(ba.gates):
                if g.ocupat is True or g.id != "-":
                    color_porta = 'red'
                else:
                    color_porta = 'green'

                if index % 2 == 0:
                    origen_X = pos_ba_X
                    final_X = pos_ba_X - 0.8
                    text_align = 'right'
                    offset_text = -0.3
                else:
                    origen_X = pos_ba_X
                    final_X = pos_ba_X + 0.8
                    text_align = 'left'
                    offset_text = 0.3

                ax.plot([origen_X, final_X], [pos_g_Y, pos_g_Y], color='blue', linewidth=2)
                ax.plot(final_X, pos_g_Y, marker='s', color=color_porta, markersize=9)

                if color_porta == 'red':
                    texto_puerta = f"{g.name} ({g.id})" if text_align == 'right' else f"{g.id} {g.name}"
                else:
                    texto_puerta = g.name

                ax.text(final_X + offset_text, pos_g_Y, texto_puerta,
                        fontsize=7, verticalalignment='center', horizontalalignment=text_align)

                if index % 2 == 1:
                    pos_g_Y -= 1.2

            pos_ba_X += 16.0

        pos_ba_X += 3.0

    pyplot.title("Estat de les Portes - Barcelona LEBL", fontsize=16, weight='bold', pad=20)
    ax.set_xlim(0, pos_ba_X)
    ax.set_ylim(y_minima_detectada - 4, 2)

    pyplot.axis('off')
    pyplot.tight_layout()
    pyplot.show()
    print("DEBUG: Estic pintant aquest aeroport:", bcn)

# Assignem una porta d'embarcament a aquells avions que passen la nit a l'aeroport (Night Aircraft).
# Sabem quins són perquè el seu origen està buit però tenen hora de sortida establerta.
def AssignNightGates(bcn, aircrafts):
    # Assigna una porta de l'aeroport a cada avió de la llista (aircrafts) que sigui només de sortida (night aircraft)
    if len(aircrafts) == 0:
        return -1

    i = 0
    while i<len(aircrafts):
        aircraft_actual = aircrafts[i]
        if (aircraft_actual.origin == "" or aircraft_actual.origin == "-") and aircraft_actual.departure_time != "":
            AssignGate(bcn,aircraft_actual)
        i += 1
    return 0

# Busquem un avió pel seu ID per totes les terminals i àrees. Quan el trobem,
# buidem la porta restablint l'estat 'ocupat = False' i el nom de l'avió a "-".
def FreeGate(bcn,id):
    # Busca l'avió amb l'id especificat en totes les portes de l'aeroport. Si el troba, allibera la porta. Si no, retorna un codi d'error.
    found = False
    i = 0
    while i<len(bcn.terminals) and not found: #Recorrem totes les terminals, areas i portes
        terminal = bcn.terminals[i]

        j = 0
        while j < len(terminal.boardingareas) and not found:
            area = terminal.boardingareas[j]

            k = 0
            while k < len(area.gates) and not found:
                gate = area.gates[k]
                if gate.id == id:
                    gate.ocupat = False
                    gate.id = "-"
                    found = True

                k += 1
            j +=1
        i += 1

    if not found: #Si no s'ha trobat cap avió, indiquem error
        return -1

    return 1 #Sinó indiquem que s'ha executat correctament

# El motor de la nostra simu horària. Primer llibera les portes de tots els avions que
# s'enlairen exactament a l'hora triada (time). Després, agafa els avions que aterren dins
# d'aquella mateixa franja d'hora (comparant els dos primers dígits "hh") i els intenta assignar porta.
# Si l'aeroport està ple, sumem +1 al comptador de vols sense porta.
def AssignGatesAtTime(bcn, aircrafts, time):
    #  Actualitza l'estat de les portes de l'aeroport per a una franja horària específica.
    # Primer allibera les portes dels avions que han marxat i després assigna portes als que arriben.
    contador_no_assig = 0
    i = 0
    while i<len(aircrafts):
        ac = aircrafts[i]
        # Si l'avió té dades de sortida i ja hauria d'haver marxat
        if ac.departure_time != "" and ac.departure_time != "-" and ac.departure_time == time:
            FreeGate(bcn,ac.aircraft_id)
        i += 1

    hora_actual = time[0:2]
    j = 0
    while j<len(aircrafts):
        ac = aircrafts[j]
        # Comprovem si l'avió aterra dins d'aquesta hora
        if ac.scheduled_time != "" and ac.scheduled_time != "-" and ac.scheduled_time[0:2] == hora_actual:
            resultat = AssignGate(bcn,ac)

        # Si AssignGate retorna un codi d'error (-1), significa que l'aeroport està ple
            if resultat == -1:
                contador_no_assig += 1
        j += 1
    return contador_no_assig


# PLOT EXTRA: Dibuixa un mapa de calor (imshow) mostrant com d'estressades estan les àrees.
# Fem una matriu on les files són les àrees d'embarcament i les columnes són les 24 hores del dia.
# Executem la simulació per a cada hora de 00:00 a 23:00, calculem el percentatge de portes
# ocupades que hi ha a cada àrea i omplim la matriu per pintar el gràfic.
def PercentatgeDOcupacio(bcn,aircrafts):
    import tkinter as tk
    # Mostra el percentatge d'ocupació de cada àrea d'embarcament per cada hora del dia.
    areas_objects = []
    areas_noms = []
    for t in bcn.terminals:
        for ba in t.boardingareas:
            areas_objects.append(ba)
            areas_noms.append(f"{t.name} - {ba.name}")

    # Fem una matriu de 24 columnes (hores del dia)
    mapa_data = []
    for _ in range(len(areas_objects)):
        mapa_data.append([0.0] * 24)

    hores = []
    for h in range(24):
        time_str = f"{h:02d}:00"
        hores.append(time_str)

        for t in bcn.terminals:
            for ba in t.boardingareas:
                for g in ba.gates:
                    g.ocupat = False
                    g.id = "-"

        print(f"-> Intentando procesar la hora: {time_str}...", end="")
        # Actualitzem l'estat de les portes per a aquesta hora específica
        AssignGatesAtTime(bcn, aircrafts, time_str)
        print(" ¡Completada con éxito!")

        # Calculem el percentatge d'ocupació de cada àrea en aquest moment
        for idx, ba in enumerate(areas_objects):
            contador_ocupat = 0
            for g in ba.gates:
                if g.ocupat:
                    contador_ocupat += 1

            # Percentatge: (portes ocupades / total de portes) * 100
            if len(ba.gates) > 0:
                percentatge = (contador_ocupat / len(ba.gates)) * 100
                mapa_data[idx][h] = percentatge

    fig, ax = pyplot.subplots(figsize=(14, 8))
    im = ax.imshow(mapa_data, cmap='YlOrRd', aspect='auto')
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Percentatge d'Ocupació (%)", rotation=-90, va="bottom")

    ax.set_xticks(range(24))
    ax.set_xticklabels(range(24))
    ax.set_yticks(range(len(areas_noms)))
    ax.set_yticklabels(areas_noms)

    pyplot.title("Mapa de Calor d'Estrès de les Àrees d'Embarcament (LEBL)", fontsize=16, pad=20)
    pyplot.xlabel("Hora del dia (hh:00)")
    pyplot.ylabel("Àrees d'Embarcament")

    pyplot.tight_layout()
    pyplot.show()

# PLOT EXTRA: Calculem l'índex de risc de congestió de l'aeroport hora per hora.
# Primer comptem el total de portes disponibles sumant-les totes.
# Després mirem quants avions arriben a cada hora i calculem el percentatge (arribades / total_portes) * 100.
# Pintem una gràfica de línies i marquem zones d'alerta de fons.
def PlotCongestionRisk(bcn, aircrafts):

    if len(aircrafts) == 0:
        print("Error: no hi ha vols")
        return
    hores = []
    risc = []               #vectors
    total_gates = 0         # Comptar totes les gates

    t = 0
    while t < len(bcn.terminals):

        terminal = bcn.terminals[t]

        a = 0
        while a < len(terminal.boardingareas):

            area = terminal.boardingareas[a]

            total_gates += len(area.gates)

            a += 1

        t += 1

    hora = 0            # Analitzar cada hora

    while hora < 24:

        arribades = 0

        i = 0
        while i < len(aircrafts):

            aircraft = aircrafts[i]

            if aircraft.scheduled_time != "":
                temps = aircraft.scheduled_time.split(":")
                h = int(temps[0])

                if h == hora:
                    arribades += 1

            i += 1

        risk_value = (arribades / total_gates) * 100 if total_gates > 0 else 0 # Càlcul del risc (%)

        hores.append(hora)
        risc.append(risk_value)

        hora += 1

    # Crear gràfic
    pyplot.figure(figsize=(12, 6))

    pyplot.plot(hores, risc, marker='o')

    # Zones de risc
    pyplot.axhspan(0, 30, alpha=0.2)
    pyplot.axhspan(30, 60, alpha=0.2)
    pyplot.axhspan(60, 100, alpha=0.2)

    pyplot.xlabel("Hour of day")
    pyplot.ylabel("Congestion Risk (%)")
    pyplot.title("Airport Congestion Risk During the Day")

    pyplot.xticks(range(0, 24))

    pyplot.grid(True)

    pyplot.show()


#ppppp
if __name__ == "__main__":

    meu_ap = BarcelonaAp("LEBL")
    t1 = Terminal("T1")
    area_a = BoardingArea("Area A", "Schengen")


    if SetGates(area_a, 1, 5, "T1A") == 0:
        t1.boardingareas.append(area_a)
        meu_ap.terminals.append(t1)
        print(f"Estructura de {meu_ap.code} amb el nom de les portes correcte.")