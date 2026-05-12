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
    Terminal = f"{t_name}_Airlines.txt"
    if not os.path.exists("Terminals.txt"):
        return -1

    terminal.airlines = []
    with open("Terminals.txt", 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                terminal.airlines.append(parts[1])
    return 0


def LoadAirportStructure(filename):
    if not os.path.exists(filename):
        return -1

    try:
        with open(filename, 'r') as f:
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
    area.gets=[]
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

    fig, ax = pyplot.subplots()
    posX = 1
    for t in bcn.terminals:
        posY = 0
        for ba in t.boardingareas:
            for g in ba.gates:
                color_porta = 'green'
                if g.ocupat:
                    color_porta = 'red'

                ax.plot(posX, posY, marker='s', color=color_porta, markersize=10)
                ax.text(posX + 0.1, posY, g.name, fontsize=8, verticalalignment='center')

                if g.ocupat:
                    ax.text(posX + 0.1, posY - 0.2, g.id, fontsize=7, color='darkred') # COHERENTE

                posY -= 1
            posY -= 2
        posX += 5

    pyplot.title("Estat de les Portes - Barcelona LEBL")
    pyplot.axis('off')
    pyplot.show()

if __name__ == "__main__":

    meu_ap = BarcelonaAp("LEBL")
    t1 = Terminal("T1")
    area_a = BoardingArea("Area A", "Schengen")


    if SetGates(area_a, 1, 5, "T1A") == 0:
        t1.boardingareas.append(area_a)
        meu_ap.terminals.append(t1)
        print(f"Estructura de {meu_ap.code} amb el nom de les portes correcte.")