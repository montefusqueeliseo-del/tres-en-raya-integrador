<<<<<<< HEAD

import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from schemas import PartidaCrear, JugadaCrear, EstadoActualizar
from database import conectar, crear_tablas


app = FastAPI(title="API del Tres en Raya")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

crear_tablas()


@app.exception_handler(sqlite3.IntegrityError)
async def error_integridad(request, exc):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "No se pudo guardar el dato en la base de datos"
        }
    )


def comprobar_ganador(tablero):
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if (
            tablero[a] != " "
            and tablero[a] == tablero[b]
            and tablero[b] == tablero[c]
        ):
            return tablero[a]

    if " " not in tablero:
        return "empate"

    return None


def obtener_tablero(conexion, partida_id):
    tablero = [" "] * 9

    jugadas = conexion.execute(
        """
        SELECT posicion, simbolo
        FROM jugadas
        WHERE partida_id = ?
        ORDER BY id
        """,
        (partida_id,)
    ).fetchall()

    for jugada in jugadas:
        tablero[jugada["posicion"] - 1] = jugada["simbolo"]

    return tablero


@app.get("/")
def inicio():
    return {"mensaje": "API del Tres en Raya funcionando"}


@app.post("/partidas", status_code=201)
def crear_partida(datos: PartidaCrear):
    conexion = conectar()

    cursor = conexion.execute(
        "INSERT INTO partidas (jugador) VALUES (?)",
        (datos.jugador,)
    )

    conexion.commit()
    partida_id = cursor.lastrowid
    conexion.close()

    return {
        "id": partida_id,
        "jugador": datos.jugador,
        "estado": "en curso"
    }


@app.get("/partidas")
def listar_partidas(jugador: str | None = None):
    conexion = conectar()

    if jugador:
        filas = conexion.execute(
            "SELECT * FROM partidas WHERE jugador LIKE ?",
            (f"%{jugador}%",)
        ).fetchall()
    else:
        filas = conexion.execute(
            "SELECT * FROM partidas"
        ).fetchall()

    conexion.close()
    return [dict(fila) for fila in filas]


@app.get("/partidas/{partida_id}")
def obtener_partida(partida_id: int):
    conexion = conectar()

    fila = conexion.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    return dict(fila)


@app.put("/partidas/{partida_id}")
def actualizar_partida(
    partida_id: int,
    datos: EstadoActualizar
):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    if partida["estado"] != "en curso":
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="La partida ya tiene un resultado registrado"
        )

    tablero = obtener_tablero(conexion, partida_id)
    resultado = comprobar_ganador(tablero)

    if datos.estado == "X ganó" and resultado != "X":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="No se puede registrar esa victoria"
        )

    if datos.estado == "O ganó" and resultado != "O":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="No se puede registrar esa victoria"
        )

    if datos.estado == "empate" and resultado != "empate":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="La partida todavía no terminó en empate"
        )

    if datos.estado == "en curso" and resultado is not None:
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="La partida ya terminó"
        )

    conexion.execute(
        "UPDATE partidas SET estado = ? WHERE id = ?",
        (datos.estado, partida_id)
    )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Estado de la partida actualizado"}


@app.delete("/partidas/{partida_id}")
def eliminar_partida(partida_id: int):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT id FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    conexion.execute(
        "DELETE FROM jugadas WHERE partida_id = ?",
        (partida_id,)
    )

    conexion.execute(
        "DELETE FROM partidas WHERE id = ?",
        (partida_id,)
    )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Partida eliminada correctamente"}


@app.post("/jugadas", status_code=201)
def registrar_jugada(datos: JugadaCrear):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (datos.partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    if partida["estado"] != "en curso":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="La partida ya terminó"
        )

    tablero = obtener_tablero(conexion, datos.partida_id)
    resultado = comprobar_ganador(tablero)

    if resultado is not None:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="La partida ya terminó"
        )

    cantidad_x = tablero.count("X")
    cantidad_o = tablero.count("O")

    if datos.simbolo == "X" and cantidad_x != cantidad_o:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="No es el turno del jugador"
        )

    if datos.simbolo == "O" and cantidad_x != cantidad_o + 1:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="No es el turno de la máquina"
        )

    if tablero[datos.posicion - 1] != " ":
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="Esa posición ya está ocupada"
        )

    cursor = conexion.execute(
        """
        INSERT INTO jugadas
        (partida_id, jugador, posicion, simbolo)
        VALUES (?, ?, ?, ?)
        """,
        (
            datos.partida_id,
            partida["jugador"] if datos.simbolo == "X" else "Máquina",
            datos.posicion,
            datos.simbolo
        )
    )

    conexion.commit()
    jugada_id = cursor.lastrowid
    conexion.close()

    return {
        "id": jugada_id,
        "partida_id": datos.partida_id,
        "posicion": datos.posicion,
        "simbolo": datos.simbolo
    }


@app.get("/partidas/{partida_id}/jugadas")
def listar_jugadas(partida_id: int):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT id FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    filas = conexion.execute(
        """
        SELECT * FROM jugadas
        WHERE partida_id = ?
        ORDER BY id
        """,
        (partida_id,)
    ).fetchall()

    conexion.close()
=======

import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from schemas import PartidaCrear, JugadaCrear, EstadoActualizar
from database import conectar, crear_tablas


app = FastAPI(title="API del Tres en Raya")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

crear_tablas()


@app.exception_handler(sqlite3.IntegrityError)
async def error_integridad(request, exc):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "No se pudo guardar el dato en la base de datos"
        }
    )


def comprobar_ganador(tablero):
    combinaciones = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if (
            tablero[a] != " "
            and tablero[a] == tablero[b]
            and tablero[b] == tablero[c]
        ):
            return tablero[a]

    if " " not in tablero:
        return "empate"

    return None


def obtener_tablero(conexion, partida_id):
    tablero = [" "] * 9

    jugadas = conexion.execute(
        """
        SELECT posicion, simbolo
        FROM jugadas
        WHERE partida_id = ?
        ORDER BY id
        """,
        (partida_id,)
    ).fetchall()

    for jugada in jugadas:
        tablero[jugada["posicion"] - 1] = jugada["simbolo"]

    return tablero


@app.get("/")
def inicio():
    return {"mensaje": "API del Tres en Raya funcionando"}


@app.post("/partidas", status_code=201)
def crear_partida(datos: PartidaCrear):
    conexion = conectar()

    cursor = conexion.execute(
        "INSERT INTO partidas (jugador) VALUES (?)",
        (datos.jugador,)
    )

    conexion.commit()
    partida_id = cursor.lastrowid
    conexion.close()

    return {
        "id": partida_id,
        "jugador": datos.jugador,
        "estado": "en curso"
    }


@app.get("/partidas")
def listar_partidas(jugador: str | None = None):
    conexion = conectar()

    if jugador:
        filas = conexion.execute(
            "SELECT * FROM partidas WHERE jugador LIKE ?",
            (f"%{jugador}%",)
        ).fetchall()
    else:
        filas = conexion.execute(
            "SELECT * FROM partidas"
        ).fetchall()

    conexion.close()
    return [dict(fila) for fila in filas]


@app.get("/partidas/{partida_id}")
def obtener_partida(partida_id: int):
    conexion = conectar()

    fila = conexion.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    return dict(fila)


@app.put("/partidas/{partida_id}")
def actualizar_partida(
    partida_id: int,
    datos: EstadoActualizar
):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    if partida["estado"] != "en curso":
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="La partida ya tiene un resultado registrado"
        )

    tablero = obtener_tablero(conexion, partida_id)
    resultado = comprobar_ganador(tablero)

    if datos.estado == "X ganó" and resultado != "X":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="No se puede registrar esa victoria"
        )

    if datos.estado == "O ganó" and resultado != "O":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="No se puede registrar esa victoria"
        )

    if datos.estado == "empate" and resultado != "empate":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="La partida todavía no terminó en empate"
        )

    if datos.estado == "en curso" and resultado is not None:
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="La partida ya terminó"
        )

    conexion.execute(
        "UPDATE partidas SET estado = ? WHERE id = ?",
        (datos.estado, partida_id)
    )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Estado de la partida actualizado"}


@app.delete("/partidas/{partida_id}")
def eliminar_partida(partida_id: int):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT id FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    conexion.execute(
        "DELETE FROM jugadas WHERE partida_id = ?",
        (partida_id,)
    )

    conexion.execute(
        "DELETE FROM partidas WHERE id = ?",
        (partida_id,)
    )

    conexion.commit()
    conexion.close()

    return {"mensaje": "Partida eliminada correctamente"}


@app.post("/jugadas", status_code=201)
def registrar_jugada(datos: JugadaCrear):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT * FROM partidas WHERE id = ?",
        (datos.partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    if partida["estado"] != "en curso":
        conexion.close()
        raise HTTPException(
            status_code=400,
            detail="La partida ya terminó"
        )

    tablero = obtener_tablero(conexion, datos.partida_id)
    resultado = comprobar_ganador(tablero)

    if resultado is not None:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="La partida ya terminó"
        )

    cantidad_x = tablero.count("X")
    cantidad_o = tablero.count("O")

    if datos.simbolo == "X" and cantidad_x != cantidad_o:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="No es el turno del jugador"
        )

    if datos.simbolo == "O" and cantidad_x != cantidad_o + 1:
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="No es el turno de la máquina"
        )

    if tablero[datos.posicion - 1] != " ":
        conexion.close()
        raise HTTPException(
            status_code=409,
            detail="Esa posición ya está ocupada"
        )

    cursor = conexion.execute(
        """
        INSERT INTO jugadas
        (partida_id, jugador, posicion, simbolo)
        VALUES (?, ?, ?, ?)
        """,
        (
            datos.partida_id,
            partida["jugador"] if datos.simbolo == "X" else "Máquina",
            datos.posicion,
            datos.simbolo
        )
    )

    conexion.commit()
    jugada_id = cursor.lastrowid
    conexion.close()

    return {
        "id": jugada_id,
        "partida_id": datos.partida_id,
        "posicion": datos.posicion,
        "simbolo": datos.simbolo
    }


@app.get("/partidas/{partida_id}/jugadas")
def listar_jugadas(partida_id: int):
    conexion = conectar()

    partida = conexion.execute(
        "SELECT id FROM partidas WHERE id = ?",
        (partida_id,)
    ).fetchone()

    if partida is None:
        conexion.close()
        raise HTTPException(
            status_code=404,
            detail="Partida no encontrada"
        )

    filas = conexion.execute(
        """
        SELECT * FROM jugadas
        WHERE partida_id = ?
        ORDER BY id
        """,
        (partida_id,)
    ).fetchall()

    conexion.close()
>>>>>>> c30926d43c46f40f7e0dfebe33f8d97fb319c235
    return [dict(fila) for fila in filas]