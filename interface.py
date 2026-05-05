import tkinter as tk
from tkinter import messagebox, filedialog
from airport import *
import aircraft as ac
from matplotlib import pyplot


class AirportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Aeroports")
        self.root.geometry("350x500")

        self.airports = []
        self.vuelos = []


        tk.Label(root, text="VERSIÓN 1: AEROPUERTOS", fg="blue").pack()
        tk.Button(root, text="Carregar Airports", command=self.load).pack(fill='x', padx=20)
        tk.Button(root, text="Actualitzar Schengen", command=self.apply_schengen).pack(fill='x', padx=20)
        tk.Button(root, text="MOSTRAR GRÀFIC SCHENGEN", command=self.draw_plot).pack(fill='x', padx=20)
        tk.Button(root, text="Google Earth", command=self.make_map).pack()

        tk.Label(root, text="VERSIÓN 2: VUELOS", fg="green").pack(pady=(10, 0))
        tk.Button(root, text="Carregar Arrivals", command=self.load_arrivals_v2).pack(fill='x', padx=20)
        tk.Button(root, text="Gràfic Arribades (Hores)", command=self.PlotArrivals).pack(fill='x', padx=20)
        tk.Button(root, text="Gràfic Aerolínies", command=self.PlotAirlines).pack(fill='x', padx=20)
        tk.Button(root, text="Gràfic Schengen (Apilat)", command=self.PlotFlightsType).pack(fill='x', padx=20)
        tk.Button(root, text="Google Earth (Tots)", command=self.make_map_v2).pack(fill='x', padx=20)
        tk.Button(root, text="Google Earth (Llarga Distància)", command=self.make_map_long_v2).pack(fill='x', padx=20)

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


    def load_arrivals_v2(self):
        self.vuelos = ac.LoadArrivals("Arrivals.txt")
        messagebox.showinfo("Info", "Arrivals actualitzat!")

    def PlotArrivals(self):
        if self.vuelos: ac.PlotArrivals(self.vuelos)

    def PlotAirlines(self):
        if self.vuelos: ac.PlotAirlines(self.vuelos)

    def PlotFlightsType(self):
        if self.vuelos: ac.PlotFlightsType(self.vuelos)

    def make_map_v2(self):
        if self.vuelos:
            ac.MapFlights(self.vuelos, "vols_tots.kml")
            messagebox.showinfo("KML", "Creat vols_tots.kml")

    def make_map_long_v2(self):
        if self.vuelos:
            vols_llargs = ac.LongDistanceArrivals(self.vuelos)
            ac.MapFlights(vols_llargs, "vols_llarga_distancia.kml")
            messagebox.showinfo("KML", f"Creat KML amb {len(vols_llargs)} vols")


if __name__ == "__main__":
    app_root = tk.Tk()
    AirportApp(app_root)
    app_root.mainloop()