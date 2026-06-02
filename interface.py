import tkinter as tk
from tkinter import messagebox, filedialog
import os
from airport import *
import aircraft as ac
from aircraft import LoadDepartures, MergeMovements, NightAircraft, PlotAverageStayTime
import matplotlib.pyplot as plt
import LEBL
from LEBL import PlotGateOccupancy, AssignGate, LoadAirportStructure, PercentatgeDOcupacio, AssignGatesAtTime, PlotCongestionRisk
import copy

class AirportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Aeroports")
        self.root.geometry("1100x900")
        self.root.configure(bg="#f4f6f9")
        self.root.minsize(1000, 800)

        self.airports = []
        self.vuelos = []
        self.vols_sortida = []
        self.vols_totals = []

        self.lebl_ap = None
        self.bcn = None
        self.all_movements = None

        BTN_FONT = ("Segoe UI", 8)
        CARD_BG = "white"


        self.scrollable_frame = tk.Frame(self.root, bg="#f4f6f9")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # GRID RESPONSIVE
        self.scrollable_frame.grid_rowconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)


        # TÍTOL

        tk.Label(self.scrollable_frame,text="GESTOR AEROPORTS",font=("Segoe UI", 15, "bold"), bg="#f4f6f9",  fg="#003366").grid(row=0, column=0, columnspan=2, pady=(5, 15))


        # COLUMNES

        left_col = tk.Frame(self.scrollable_frame, bg="#f4f6f9")
        right_col = tk.Frame(self.scrollable_frame, bg="#f4f6f9")

        left_col.grid(row=1, column=0, sticky="nsew", padx=10)
        right_col.grid(row=1, column=1, sticky="nsew", padx=10)


        #  COLUMNA ESQUERRA
        #Versio 1
        frame1 = tk.LabelFrame(left_col, text="VERSIÓ 1 · AEROPUERTOS", font=("Segoe UI", 10, "bold"),bg=CARD_BG, fg="#1565C0",   padx=10,  pady=10  )
        frame1.pack(fill="both", expand=True, pady=10)

        # Botons versio 1
        tk.Button(frame1, text="Carregar Airports", command=self.load, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame1, text="Actualitzar Schengen", command=self.apply_schengen, font=BTN_FONT).pack(fill='x',pady=2)
        tk.Button(frame1, text="Mostrar Gràfic Schengen", command=self.draw_plot, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame1, text="Google Earth", command=self.make_map, font=BTN_FONT).pack(fill='x', pady=2)

        #Versio 3
        frame3 = tk.LabelFrame( left_col,  text="VERSIÓ 3 · GESTIÓN DE PUERTAS",font=("Segoe UI", 10, "bold"),  bg=CARD_BG,   fg="#EF6C00",  padx=10,  pady=10 )
        frame3.pack(fill="both", expand=True, pady=10)


        # Botons versio 3
        tk.Button(frame3, text="Carregar LEBL", command=self.load_lebl_v3, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame3, text="Assignar Portes a Arribades", command=self.assign_gates_v3, font=BTN_FONT).pack( fill='x', pady=2)
        tk.Button(frame3, text="Mapa d'Ocupació de Portes", command=self.show_map, font=BTN_FONT).pack(fill='x', pady=2)

        # COLUMNA DRETA
        #Versio 2
        frame2 = tk.LabelFrame(right_col, text="VERSIÓ 2 · VUELOS",font=("Segoe UI", 10, "bold"), bg=CARD_BG,  fg="#2E7D32",padx=10,  pady=10  )

        frame2.pack(fill="both", expand=True, pady=10)
        # Botons versio 2
        tk.Button(frame2, text="Carregar Arrivals", command=self.load_arrivals_v2, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame2, text="Gràfic Arribades (Hores)", command=self.PlotArrivals, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame2, text="Gràfic Aerolínies", command=self.PlotAirlines, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame2, text="Gràfic Schengen (Apilat)", command=self.PlotFlightsType, font=BTN_FONT).pack(fill='x',                                                                                              pady=2)
        tk.Button(frame2, text="Google Earth (Tots)", command=self.make_map_v2, font=BTN_FONT).pack(fill='x', pady=2)


        #versio 4
        frame4 = tk.LabelFrame( right_col, text="VERSIÓ 4 · SIMULACIÓ", font=("Segoe UI", 10, "bold"),bg=CARD_BG, fg="#6A1B9A",  padx=10,  pady=10)
        frame4.pack(fill="both", expand=True, pady=10)

        #Botons versio 4
        tk.Button(frame4, text="Carregar Sortides", command=self.gui_load_departures_v4, font=BTN_FONT).pack(fill='x',  pady=2)
        tk.Button(frame4, text="Fusionar Moviments", command=self.gui_merge_movements_v4, font=BTN_FONT).pack(fill='x',     pady=2)
        tk.Label(frame4, text="Hora de simulació (hh:00)", bg=CARD_BG).pack(pady=(8, 0))

        self.hora_var = tk.StringVar(value="08:00")
        tk.Entry(frame4, textvariable=self.hora_var, justify='center', font=("Segoe UI", 10)).pack(fill='x', pady=5)
        tk.Button(frame4, text="Assignar Portes a l'Hora Triada", command=self.assignar_v4, bg="#E3F2FD").pack(fill='x',                                                                                                  pady=3)
        tk.Button(frame4, text="Simular (Assignar Portes)", command=self.mostrar_mapa_v4, bg="#6A1B9A",fg="white").pack(fill='x', pady=3)



        #Polts extres
        frame5 = tk.LabelFrame( right_col,text="PLOTS EXTRES",  font=("Segoe UI", 10, "bold"), bg=CARD_BG,fg="#C62828",  padx=10,  pady=10  )
        frame5.pack(fill="both", expand=True, pady=10)

        # Botons plots extres
        tk.Button(frame5, text="Percentatge d'Ocupació", command=self.show_occupancy_percentage, font=BTN_FONT).pack(fill='x', pady=2)
        tk.Button(frame5, text="Estadistica de estada", command=self.executar_plot_estada, font=BTN_FONT).pack(fill='x',pady=2)
        tk.Button(frame5, text="Risc de Congestió", command=self.show_congestion_risk, font=BTN_FONT).pack(fill='x',pady=2)



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

        plt.figure("Estadístiques Schengen")
        plt.bar(['Airports'], [s_count], color='green', label='Schengen')
        plt.bar(['Airports'], [ns_count], bottom=[s_count], color='red', label='No Schengen')
        plt.ylabel('Quantitat')
        plt.title('Aeroports Schengen vs No Schengen')
        plt.legend()
        plt.show()

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
            ac.MapFlights(self.vuelos, "Google Earth/vols_tots.kml")
            messagebox.showinfo("KML", "Creat vols_tots.kml")

    def make_map_long_v2(self):
        if self.vuelos:
            vols_llargs = ac.LongDistanceArrivals(self.vuelos)
            ac.MapFlights(vols_llargs, "Google Earth/vols_llarga_distancia.kml")
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

    def show_congestion_risk(self):

        if not self.lebl_ap:
            messagebox.showwarning("Atenció","Cal carregar l'aeroport primer.")
            return

        if not self.vols_totals:
            messagebox.showwarning("Atenció","Cal fusionar els moviments primer.")
            return

        PlotCongestionRisk(self.lebl_ap, self.vols_totals)

if __name__ == "__main__":
    app_root = tk.Tk()
    AirportApp(app_root)
    app_root.mainloop()