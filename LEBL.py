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
