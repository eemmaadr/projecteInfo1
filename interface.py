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
        tk.Button(root, text="Carregar Airports.txt", command=self.load).pack(fill='x', padx=20)
        tk.Button(root, text="Actualitzar Schengen", command=self.apply_schengen).pack(fill='x', padx=20)
        tk.Button(root, text="MOSTRAR GRÀFIC SCHENGEN", command=self.draw_plot).pack(fill='x', padx=20)


        tk.Label(root, text="VERSIÓN 2: VUELOS", fg="green").pack(pady=(10, 0))
        tk.Button(root, text="Carregar Arrivals.txt", command=self.load_arrivals_v2).pack(fill='x', padx=20)
        tk.Button(root, text="Gràfic Arribades (Hores)", command=self.plot_hours_v2).pack(fill='x', padx=20)
        tk.Button(root, text="Gràfic Aerolínies", command=self.plot_airlines_v2).pack(fill='x', padx=20)
        tk.Button(root, text="Gràfic Schengen (Apilat)", command=self.plot_schengen_v2).pack(fill='x', padx=20)
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
        s_count = sum(1 for a in self.airports if a.Schengen)
        ns_count = len(self.airports) - s_count
        pyplot.figure("Estadístiques Schengen")
        pyplot.bar(['Airports'], [s_count], color='blue', label='Schengen')
        pyplot.bar(['Airports'], [ns_count], bottom=[s_count], color='red', label='No Schengen')
        pyplot.legend();
        pyplot.show()



    def load_arrivals_v2(self):
        f = filedialog.askopenfilename()
        if f:
            self.vuelos = ac.LoadArrivals(f)
            messagebox.showinfo("Info", f"Carregats {len(self.vuelos)} vols!")

    def plot_hours_v2(self):
        if self.vuelos: ac.PlotArrivals(self.vuelos)

    def plot_airlines_v2(self):
        if self.vuelos: ac.PlotAirlines(self.vuelos)

    def plot_schengen_v2(self):
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