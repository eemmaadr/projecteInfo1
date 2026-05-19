import matplotlib.pyplot as pyplot
import math
import os
import matplotlib.pyplot as plt

class BarcelonaAp:
    def __init__(self,code):
        self.code = code
        self.terminals= []
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
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


def LoadAirlines(terminal, t_name):

    filename = t_name + "_Airlines.txt"

    if not os.path.exists(filename):
        return -1

    airlines_list = []

    with open(filename, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if line != "":

                parts = line.split("\t")

                if len(parts) >= 2:

                    airline_code = parts[1]

                    airlines_list.append(airline_code)

    terminal.airlines = airlines_list

    return 0

def LoadAirportStructure(filename):

    if not os.path.exists(filename):
        return -1

    with open(filename, "r", encoding="utf-8") as file:

        first_line = file.readline().strip().split()

        airport_code = first_line[0]

        num_terminals = int(first_line[1])

        bcn = BarcelonaAp(airport_code)

        for i in range(num_terminals):

            terminal_line = file.readline().strip().split()

            terminal_name = terminal_line[1]

            num_areas = int(terminal_line[2])

            terminal = Terminal(terminal_name)

            LoadAirlines(terminal, terminal_name)

            for j in range(num_areas):

                area_line = file.readline().strip().split()

                area_name = area_line[1]

                area_type = area_line[2]

                init_gate = int(area_line[4])

                end_gate = int(area_line[6])

                area = BoardingArea(area_name, area_type)

                prefix = terminal_name + "BA" + area_name + "G"

                SetGates(area, init_gate, end_gate, prefix)

                terminal.boarding_areas.append(area)

            bcn.terminals.append(terminal)

    return bcn


def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name

    return ""


def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.airline)
    if terminal_name == "":
        return -1
    schengen_airports = [
        "LEMD", "LFPG", "LIRF", "EDDF",
        "EHAM", "LPPT", "LOWW"
    ]
    if aircraft.origin in schengen_airports:
        required_type = "Schengen"
    else:
        required_type = "non-Schengen"
    for terminal in bcn.terminals:
        if terminal.name == terminal_name:
            for area in terminal.boarding_areas:
                if area.type == required_type:
                    for gate in area.gates:
                        if gate.ocupat == False:
                            gate.ocupat = True
                            gate.aircraft_id = aircraft.aircraft_id
                            return 0

    return -1

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
        return False, -1

    if not terminal.airlines:
         return False
    if name in terminal.airlines:
     return True
    else:
        return False

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

def PlotGateOccupancy(bcn):

    fig, ax = plt.subplots(figsize=(14, 6))

    x_terminal = 0

    for terminal in bcn.terminals:

        # Barra horizontal superior del terminal
        ax.plot(
            [x_terminal, x_terminal + 12],
            [10, 10],
            linewidth=14,
            color="#0B5A7A"
        )
        ax.text(
            x_terminal - 1,
            10,
            terminal.name,
            fontsize=16
        )
        x_area = x_terminal + 1
        for area in terminal.boarding_areas:
            # Columna vertical boarding area
            ax.plot(
                [x_area, x_area],
                [2, 10],
                linewidth=14,
                color="#0B5A7A"
            )
            ax.text(
                x_area - 0.4,
                1,
                terminal.name + "BA" + area.name,
                fontsize=10
            )
            y_gate = 8
            for gate in area.gates:
                # pequeña línea horizontal gate
                ax.plot(
                    [x_area - 0.8, x_area],
                    [y_gate, y_gate],
                    linewidth=3,
                    color="#0B5A7A"
                )
                # color ocupación
                if gate.ocupat:
                    color = "red"
                else:
                    color = "green"
                # cuadrado gate
                ax.plot(
                    x_area - 1.2,
                    y_gate,
                    marker="s",
                    markersize=8,
                    color=color
                )
                # mostrar nombre solo algunas veces
                if gate.name.endswith("1") or gate.name.endswith("3"):
                    ax.text(
                        x_area + 0.2,
                        y_gate,
                        gate.name,
                        fontsize=8
                    )
                # aircraft ID
                if gate.ocupat:
                    ax.text(
                        x_area - 2.2,
                        y_gate,
                        gate.aircraft_id,
                        fontsize=8
                    )
                y_gate -= 0.8
                # limitar altura
                if y_gate < 2:
                    break
            x_area += 4
        x_terminal += 18
    plt.title("Estat de les Portes - Barcelona LEBL")

    plt.axis("off")

    plt.show()


def NonSchengenArrivals(llista_vols):
    llista_schengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY',
                       'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    vols_filtrats = []

    for vol in llista_vols:
        prefix = vol.origin[:2]
        if prefix not in llista_schengen:
            vols_filtrats.append(vol)

    return vols_filtrats
if __name__ == "__main__":

    meu_ap = BarcelonaAp("LEBL")
    t1 = Terminal("T1")
    area_a = BoardingArea("Area A", "Schengen")


    if SetGates(area_a, 1, 5, "T1A") == 0:
        t1.boardingareas.append(area_a)
        meu_ap.terminals.append(t1)
        print(f"Estructura de {meu_ap.code} amb el nom de les portes correcte.")