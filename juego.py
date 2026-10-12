<<<<<<< HEAD
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
            return "La partida ya terminó."

        if self.turno != "X":
            return "No es tu turno."

        if posicion < 1 or posicion > 9:
            return "Elegí una posición del 1 al 9."

        indice = posicion - 1

        if self.tablero[indice] != " ":
            return "Esa posición ya está ocupada."

        self.tablero[indice] = "X"
        resultado = self.comprobar_ganador()

        if resultado:
            self.estado = resultado
            return "¡Ganaste!" if resultado == "X" else "¡Empate!"

        self.turno = "O"
        return "Jugaste X."

    def turno_maquina(self):
        if self.estado != "en curso":
            return "La partida ya terminó."

        if self.turno != "O":
            return "Todavía no es el turno de la máquina."

        libres = [
            i for i in range(9)
            if self.tablero[i] == " "
        ]

        if not libres:
            self.estado = "Empate"
            return "¡Empate!"

        posicion = random.choice(libres)
        self.tablero[posicion] = "O"

        resultado = self.comprobar_ganador()

        if resultado:
            self.estado = resultado
            return (
                "La máquina ganó."
                if resultado == "O"
                else "¡Empate!"
            )

        self.turno = "X"
=======
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
            return "La partida ya terminó."

        if self.turno != "X":
            return "No es tu turno."

        if posicion < 1 or posicion > 9:
            return "Elegí una posición del 1 al 9."

        indice = posicion - 1

        if self.tablero[indice] != " ":
            return "Esa posición ya está ocupada."

        self.tablero[indice] = "X"
        resultado = self.comprobar_ganador()

        if resultado:
            self.estado = resultado
            return "¡Ganaste!" if resultado == "X" else "¡Empate!"

        self.turno = "O"
        return "Jugaste X."

    def turno_maquina(self):
        if self.estado != "en curso":
            return "La partida ya terminó."

        if self.turno != "O":
            return "Todavía no es el turno de la máquina."

        libres = [
            i for i in range(9)
            if self.tablero[i] == " "
        ]

        if not libres:
            self.estado = "Empate"
            return "¡Empate!"

        posicion = random.choice(libres)
        self.tablero[posicion] = "O"

        resultado = self.comprobar_ganador()

        if resultado:
            self.estado = resultado
            return (
                "La máquina ganó."
                if resultado == "O"
                else "¡Empate!"
            )

        self.turno = "X"
>>>>>>> c30926d43c46f40f7e0dfebe33f8d97fb319c235
        return f"La máquina jugó en la posición {posicion + 1}."