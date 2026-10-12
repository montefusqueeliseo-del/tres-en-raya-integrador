import random


class Partida:
    def __init__(self):
        self.tablero = [" "] * 9
        self.turno = "X"
        self.estado = "en curso"

    def mostrar_tablero(self):
        for fila in range(3):
            inicio = fila * 3
            print(
                self.tablero[inicio], "|",
                self.tablero[inicio + 1], "|",
                self.tablero[inicio + 2]
            )
            if fila < 2:
                print("--+---+--")

    def comprobar_ganador(self):
        combinaciones = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in combinaciones:
            if (
                self.tablero[a] != " "
                and self.tablero[a] == self.tablero[b]
                and self.tablero[b] == self.tablero[c]
            ):
                return self.tablero[a]

        if " " not in self.tablero:
            return "Empate"

        return None

    def jugar(self, posicion):
        if self.estado != "en curso":
            return "La partida ya termin├│."

        if self.turno != "X":
            return "No es tu turno."

        if posicion < 1 or posicion > 9:
            return "Eleg├¡ una posici├│n del 1 al 9."

        indice = posicion - 1

        if self.tablero[indice] != " ":
            return "Esa posici├│n ya est├í ocupada."

        self.tablero[indice] = "X"
        resultado = self.comprobar_ganador()

        if resultado:
            self.estado = resultado
            return "┬íGanaste!" if resultado == "X" else "┬íEmpate!"

        self.turno = "O"
        return "Jugaste X."

    def turno_maquina(self):
        if self.estado != "en curso":
            return "La partida ya termin├│."

        if self.turno != "O":
            return "Todav├¡a no es el turno de la m├íquina."

        libres = [
            i for i in range(9)
            if self.tablero[i] == " "
        ]

        if not libres:
            self.estado = "Empate"
            return "┬íEmpate!"

        posicion = random.choice(libres)
        self.tablero[posicion] = "O"

        resultado = self.comprobar_ganador()

        if resultado:
            self.estado = resultado
            return (
                "La m├íquina gan├│."
                if resultado == "O"
                else "┬íEmpate!"
            )

        self.turno = "X"
        return f"La m├íquina jug├│ en la posici├│n {posicion + 1}."
