import tkinter as tk
from tkinter import messagebox, filedialog
import os
from airport import *
import aircraft as ac
from matplotlib import pyplot
import LEBL
from LEBL import PlotGateOccupancy, AssignGate, LoadAirportStructure, PercentatgeDOcupacio, AssignGatesAtTime
from aircraft import LoadDepartures, MergeMovements, NightAircraft, PlotAverageStayTime
import copy

class AirportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Aeroports")
        self.root.geometry("350x700")

        self.airports = []
        self.vuelos = []
        self.vols_sortida = []  # Llista de sortides
        self.vols_totals = []  # Llista fusionada
        self.lebl_ap = None
        self.bcn = None
        self.all_movements= None

        tk.Label(self.root, text="VERSIÓN 1: AEROPUERTOS", fg="blue").pack()
        tk.Button(self.root, text="Carregar Airports", command=self.load).pack(fill='x', padx=20)
        tk.Button(self.root, text="Actualitzar Schengen", command=self.apply_schengen).pack(fill='x', padx=20)
        tk.Button(self.root, text="MOSTRAR GRÀFIC SCHENGEN", command=self.draw_plot).pack(fill='x', padx=20)
        tk.Button(self.root, text="Google Earth", command=self.make_map).pack()

        tk.Label(self.root, text="VERSIÓN 2: VUELOS", fg="green").pack(pady=(10, 0))
        tk.Button(self.root, text="Carregar Arrivals", command=self.load_arrivals_v2).pack(fill='x', padx=20)
        tk.Button(self.root, text="Gràfic Arribades (Hores)", command=self.PlotArrivals).pack(fill='x', padx=20)
        tk.Button(self.root, text="Gràfic Aerolínies", command=self.PlotAirlines).pack(fill='x', padx=20)
        tk.Button(self.root, text="Gràfic Schengen (Apilat)", command=self.PlotFlightsType).pack(fill='x', padx=20)
        tk.Button(self.root, text="Google Earth (Tots)", command=self.make_map_v2).pack(fill='x', padx=20)
        tk.Button(self.root, text="Google Earth (Llarga Distància)", command=self.make_map_long_v2).pack(fill='x', padx=20)

        tk.Label(self.root, text="VERSIÓN 3: GESTIÓN DE PUERTAS", fg="orange").pack(pady=(10, 0))
        tk.Button(self.root, text="Carregar Estructura LEBL", command=self.load_lebl_v3).pack(fill='x', padx=20)
        tk.Button(self.root, text="Assignar Portes a Arribades", command=self.assign_gates_v3).pack(fill='x', padx=20)
        tk.Button(self.root, text="Mapa d'Ocupació de Portes", command=self.show_map).pack(fill='x', padx=20)



        tk.Label(self.root, text="VERSIÓ 4: SIMULACIÓ DINÀMICA", fg="purple", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        tk.Button(self.root, text="Carregar Sortides ",command=self.gui_load_departures_v4).pack(fill='x', padx=20, pady=2)
        tk.Button(self.root, text="Fusionar Moviments ",command=self.gui_merge_movements_v4).pack(fill='x', padx=20, pady=2)
        tk.Label(self.root, text="Hora de simulació (hh:00):").pack()
        self.hora_var = tk.StringVar(value="08:00")
        tk.Entry(self.root, textvariable=self.hora_var, justify='center').pack(fill='x', padx=20)
        tk.Button(self.root, text="Assignar Portes a l'Hora Triada", command=self.assignar_v4, bg="#e1f5fe").pack(fill='x', padx=20, pady=5)
        tk.Button(self.root, text="Simular  (Assignar Portes)",command=self.mostrar_mapa_v4, bg="purple", fg="white").pack(fill='x', padx=20, pady=5)
        #PLOTS EXTRES


        tk.Label(self.root, text="PLOTS EXTRES", fg="red").pack(pady=(10, 0))
        tk.Button(self.root, text="Percentatge d'Ocupació", command=self.show_occupancy_percentage).pack(fill='x', padx=20)
        tk.Button(self.root, text="Estadistica de estada", command=self.executar_plot_estada).pack(fill='x', padx=20)

    def eliminar_cercanos(self):
        if not self.vuelos:
            messagebox.showwarning("Aviso", "No hay vuelos cargados.")
            return


        self.vuelos = ac.Filtro(self.vuelos, "filtrados_1000km.kml")

        messagebox.showinfo("Proceso completado", f"Vuelos restantes: {len(self.vuelos)}. Se ha generado el archivo KML.")


    def show_map(self):
        if self.lebl_ap is not None:
            # Llamamos a la función con el ajuste de escala dinámico
            PlotGateOccupancy(self.lebl_ap)
        else:
            messagebox.showwarning("Atenció", "Primer has de carregar l'estructura LEBL (Botó de la VERSIÓN 3).")

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

    def load_lebl_v3(self):
        self.lebl_ap = LoadAirportStructure("Terminals.txt")
        if self.lebl_ap:
            messagebox.showinfo("Info", "Estructura de l'aeroport carregada!")
        else:
            messagebox.showerror("Error", "No s'ha pogut carregar l'estructura.")


    def assign_gates_v3(self):
        if not self.lebl_ap or not self.vuelos:
            messagebox.showwarning("Atenció", "Cal carregar l'aeroport i els vols primer.")
            return

        vols_sense_porta = 0
        for vol in self.vuelos:
            resultat = AssignGate(self.lebl_ap, vol)
            if resultat == -1:
                vols_sense_porta += 1

        messagebox.showinfo("Assignació", f"Procés finalitzat. Vols sense porta: {vols_sense_porta}")

    def show_occupancy_v3(self):
        if not self.lebl_ap:
            messagebox.showwarning("Atenció", "Carrega l'aeroport primer.")
            return
        PlotGateOccupancy(self.lebl_ap)

    def show_occupancy_percentage(self):
        if not self.lebl_ap or not self.vuelos:
            messagebox.showwarning("Atenció", "Cal carregar l'aeroport (V3) i els vols (V2) primer.")
            return

        # Llamamos a la función importada de LEBL.py pasando la estructura y los vuelos
        PercentatgeDOcupacio(self.lebl_ap, self.vuelos)

    def executar_plot_estada(self):

        if hasattr(self, 'vols_totals') and self.vols_totals:
            PlotAverageStayTime(self.vols_totals)
        else:
            messagebox.showwarning("Atenció", "Primer cal fusionar els moviments.")


    def gui_load_departures_v4(self):

        # Crida a la funció obligatòria LoadDepartures
        self.vols_sortida, error = LoadDepartures("Departures.txt")

        if error == -1:
            messagebox.showerror("Error de Robustesa", "No s'ha trobat el fitxer Departures.txt")
        else:
            messagebox.showinfo("Èxit", f"S'han carregat {len(self.vols_sortida)} vols de sortida.")

    def gui_merge_movements_v4(self):

            # Evitar que l'app s'aturi si falten fitxers
            if not self.vuelos or not self.vols_sortida:
                messagebox.showwarning("Atenció",
                                       "Cal carregar Arrivals  i Departures  abans de fusionar.")
                return

            # Utilitzem self.vols_totals per guardar el resultat de la fusió.
            self.vols_totals, error = MergeMovements(self.vuelos, self.vols_sortida)

            if error == 0:
                messagebox.showinfo("Integració", "Moviments fusionats correctament.")
            else:
                messagebox.showerror("Error", "S'ha produït un error en la fusió.")

    def assignar_v4(self):

        #Comprovem que l'aeroport (V3) i els vols fusionats (V4) estiguin a punt [1].
        if self.lebl_ap is None or not self.vols_totals:
            messagebox.showwarning("Atenció", "Cal carregar l'estructura (LEBL.txt) i fusionar els moviments primer.")
            return

        for t in self.lebl_ap.terminals:
            for ba in t.boardingareas:
                for g in ba.gates:
                    g.ocupat = False
                    g.id = "-"  # Reset de l'ID de l'avió

        # Obtenim l'hora de l'Entry (ex: "08:00") i cridem la funció dinàmica.
        hora = self.hora_var.get()
        pendents = AssignGatesAtTime(self.lebl_ap, self.vols_totals, hora)

        messagebox.showinfo("Assignació",
                            f"Simulació a les {hora} completada.\n"
                            f"Vols sense porta per falta d'espai: {pendents}\n"
                            "Ja pots prémer 'Mostrar Mapa' per veure el resultat visual.")


    def mostrar_mapa_v4(self):
        if self.lebl_ap is None:
            messagebox.showwarning("Atenció", "Primer has de carregar l'aeroport (V3).")
            return
        ocupades_reals = 0
        total = 0
        for t in self.lebl_ap.terminals:
            for ba in t.boardingareas:
                for g in ba.gates:
                    total += 1
                    # si té ID, està ocupat
                    if hasattr(g, 'id') and g.id != "-":
                        g.ocupat = True
                        ocupades_reals += 1
                    else:
                        g.ocupat = False
                        g.id = "-"

        #Creem una còpia profunda per al mapa
        # Això evita que qualsevol bug intern de PlotGateOccupancy modifiqui la teva simulació
        bcn_per_al_mapa = copy.deepcopy(self.lebl_ap)
        # Dibuixem amb la còpia
        PlotGateOccupancy(bcn_per_al_mapa)

        #Informem amb els números que hem calculat a la simulació real
        messagebox.showinfo("Resultat Visual",
                            f"Estadístiques del sistema:\n"
                            f"- Portes Ocupades (Vermell): {ocupades_reals}\n"
                            f"- Portes Lliures (Verd): {total - ocupades_reals}")
if __name__ == "__main__":
    app_root = tk.Tk()
    AirportApp(app_root)
    app_root.mainloop()