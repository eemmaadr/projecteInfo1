from airport import *

print("--- TEST PAS 2 ---")
mi_ap = Airport("LEBL", 41.297445, 2.0832941)
SetSchengen(mi_ap)
PrintAirport(mi_ap)

print("\n--- TEST PAS 4 ---")
llista = LoadAirports("Airports.txt")
if len(llista) > 0:
    print("S'han carregat", len(llista), "aeroports.")
    for ap in llista:
        SetSchengen(ap)
    PlotAirports(llista)
    MapAirports(llista)
