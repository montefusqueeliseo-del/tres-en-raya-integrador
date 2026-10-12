from juego import Partida

partida = Partida()

print("=== TRES EN RAYA ===")
print("Vos sos X y la m├íquina es O.")
print("Las posiciones son:")
print("1 | 2 | 3")
print("--+---+--")
print("4 | 5 | 6")
print("--+---+--")
print("7 | 8 | 9")

while partida.estado == "en curso":
    print()
    partida.mostrar_tablero()

    try:
        posicion = int(input("Eleg├¡ una posici├│n del 1 al 9: "))
    except ValueError:
        print("Ten├®s que ingresar un n├║mero.")
        continue

    print(partida.jugar(posicion))

    if partida.estado != "en curso":
        break

    print(partida.turno_maquina())

print()
partida.mostrar_tablero()
print("Fin de la partida:", partida.estado)
