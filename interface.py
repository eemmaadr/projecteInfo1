import tkinter as tk
from tkinter import messagebox
from airport import *


class AirportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Aeroports")
        self.airports = []

        # Botons
        tk.Button(root, text="Carregar Airports.txt", command=self.load).pack()
        tk.Button(root, text="Actualitzar Schengen", command=self.apply_schengen).pack()
        tk.Button(root, text="MOSTRAR GRÀFIC", command=self.draw_plot).pack()
        tk.Button(root, text="Google Earth", command=self.make_map).pack()

    def load(self):
        self.airports = LoadAirports("Airports.txt")
        messagebox.showinfo("Info", "Carregats!")

    def apply_schengen(self):
        for a in self.airports: SetSchengen(a)
        messagebox.showinfo("Info", "Schengen actualitzat!")

    def draw_plot(self):
        if not self.airports: return

        s_count = 0
        ns_count = 0
        for a in self.airports:
            if a.Schengen:
                s_count += 1
            else:
                ns_count += 1

        pyplot.figure("Estadístiques Schengen")
        pyplot.bar(['Airports'], [s_count], color='blue', label='Schengen')
        pyplot.bar(['Airports'], [ns_count], bottom=[s_count], color='red', label='No Schengen')
        pyplot.ylabel('Quantitat')
        pyplot.title('Aeroports Schengen vs No Schengen')
        pyplot.legend()
        pyplot.show()

    def make_map(self):
        MapAirports(self.airports)
        messagebox.showinfo("KML", "Fitxer creat!")

if __name__ == "__main__":
    app_root = tk.Tk()
    AirportApp(app_root)
    app_root.mainloop()