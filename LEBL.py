import matplotlib.pyplot as pyplot
import math

class BarcelonaAp:
    def __init__(self,code):
        self.code = code
        self.terminals= []
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boardingarea=[]
        self.airlines=[]
class BoardingArea:
    def __init__(self,name,type):
        self.name = name
        self.type = type
        self.gates=[]
class Gate:
    def __init__(self,name):
        self.name = name
        self.opcuat= False
        self.id="-"


def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"
    if not os.path.exists(filename):
        return -1

    terminal.airlines = []
    with open(filename, 'r') as f:
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
            bcn = BarcelonaAP(header[0])
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
                    terminal.boarding_areas.append(area)

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
            for area in terminal.boarding_areas:
                if area.type == aircraft.type:
                    for gate in area.gates:
                        if not gate.is_occupied:
                            gate.is_occupied = True
                            gate.aircraft_id = aircraft.id
                            return 0
    return -1