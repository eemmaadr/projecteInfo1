import matplotlib.pyplot as pyplot
import math
import os

class BarcelonaAp:
    def __init__(self,code):
        self.code = code
        self.terminals= []
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boardingareas=[]
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
    "Terminals.txt" = f"{t_name}_Airlines.txt"
    if not os.path.exists("Terminals.txt"):
        return -1

    terminal.airlines = []
    with open("Terminals.txt", 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                terminal.airlines.append(parts[1])
    return 0


def LoadAirportStructure(Terminal):
    if not os.path.exists(Terminal):
        return -1

    try:
        with open("Terminal.txt", 'r') as f:
            header = f.readline().split()
            bcn = BarcelonaAp(header[0])
            num_terminals = int(header[1])

            for _ in range(num_terminals):
                t_line = f.readline().split()
                t_name = t_line[1]
                num_areas = int(t_line[2])

                terminal = Terminal(t_name)
                LoadAirlines(terminal, t_name)

                for _ in range(num_areas):
                    a_line = f.readline().split()
                    a_name = a_line[1]
                    a_type = a_line[2]
                    i_gate = int(a_line[4])
                    e_gate = int(a_line[6])

                    area = BoardingArea(a_name, a_type)
                    SetGates(area, i_gate, e_gate, f"{t_name}{a_name}G")
                    terminal.boardingareas.append(area)

                bcn.terminals.append(terminal)
        return bcn
    except:
        return -1


def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name
    return ""


def AssignGate(bcn, aircraft):
    target_terminal = SearchTerminal(bcn, aircraft.airline)

    if target_terminal == "":
        return -1

    for terminal in bcn.terminals:
        if terminal.name == target_terminal:
            for area in terminal.boardingareas:
                if area.type == aircraft.type:
                    for gate in area.gates:
                        if not gate.ocupat:
                            gate.ocupat= True
                            gate.id = aircraft.id
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
    if not bcn or not bcn.terminals:
        print("Error: No hi ha dades de l'aeroport.")
        return

    fig, ax = pyplot.subplots(figsize=(16, 9))

    pos_ba_X = 2
    # Variable para registrar el punto más bajo al que llega cualquier pasillo
    y_minima_detectada = -26

    for t in bcn.terminals:
        # T1 arriba (y_base = 0), T2 abajo (y_base = -10)
        y_base = 0 if "1" in t.name else -10

        largo_barra = len(t.boardingareas) * 4
        ax.plot([pos_ba_X - 1, pos_ba_X + largo_barra - 3], [y_base, y_base], color='blue', linewidth=6,
                solid_capstyle='butt')
        ax.text(pos_ba_X - 1.5, y_base, t.name, fontsize=14, weight='bold', verticalalignment='center')

        for ba in t.boardingareas:
            letra_zona = ba.name.replace(t.name + "BA", "").upper()
            if not letra_zona:
                letra_zona = ba.name

            # Dibujamos el pasillo vertical
            max_puertas = len(ba.gates)
            largo_pasillo = max(7, (max_puertas // 2) * 1.3)

            punto_final_pasillo = y_base - largo_pasillo
            # Registramos si este pasillo baja más que el mínimo actual para ajustar el zoom al final
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

                # Alternamos lados del pasillo
                if index % 2 == 0:
                    origen_X = pos_ba_X
                    final_X = pos_ba_X - 0.6
                    text_align = 'right'
                    offset_text = -0.25
                else:
                    origen_X = pos_ba_X
                    final_X = pos_ba_X + 0.6
                    text_align = 'left'
                    offset_text = 0.25

                # Dibujamos el conector azul (finger)
                ax.plot([origen_X, final_X], [pos_g_Y, pos_g_Y], color='blue', linewidth=2)

                # Dibujamos el cuadrado del estado
                ax.plot(final_X, pos_g_Y, marker='s', color=color_porta, markersize=9)

                # Texto dinámico según el color
                if color_porta == 'red':
                    texto_puerta = f"{g.name} ({g.id})" if text_align == 'right' else f"{g.id} {g.name}"
                else:
                    texto_puerta = g.name

                ax.text(final_X + offset_text, pos_g_Y, texto_puerta,
                        fontsize=7, verticalalignment='center', horizontalalignment=text_align)

                if index % 2 == 1:
                    pos_g_Y -= 1.2

            pos_ba_X += 4.5

        pos_ba_X += 1.5

    # Ajustes de la ventana y el título
    pyplot.title("Estat de les Portes - Barcelona LEBL", fontsize=16, weight='bold', pad=20)
    ax.set_xlim(0, pos_ba_X)

    # --- AQUÍ ESTÁ EL TRUCO ---
    # Usamos la Y más baja detectada dinámicamente dándole un margen extra (-3) para las etiquetas de las letras
    ax.set_ylim(y_minima_detectada - 3, 2)

    pyplot.axis('off')
    pyplot.tight_layout()
    pyplot.show()

if __name__ == "__main__":

    meu_ap = BarcelonaAp("LEBL")
    t1 = Terminal("T1")
    area_a = BoardingArea("Area A", "Schengen")

    if SetGates(area_a, 1, 5, "T1A") == 0:
        t1.boardingareas.append(area_a)
        meu_ap.terminals.append(t1)
        print(f"Estructura de {meu_ap.code} amb el nom de les portes correcte.")