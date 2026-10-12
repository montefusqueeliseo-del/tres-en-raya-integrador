<<<<<<< HEAD
import sqlite3

DB_NAME = "tres_en_raya.db"


def conectar():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'en curso'
        )
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS jugadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            jugador TEXT NOT NULL,
            posicion INTEGER NOT NULL,
            simbolo TEXT NOT NULL,
            FOREIGN KEY (partida_id) REFERENCES partidas(id)
        )
    """)

    conexion.commit()
    conexion.close()
=======
import sqlite3

DB_NAME = "tres_en_raya.db"


def conectar():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'en curso'
        )
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS jugadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            jugador TEXT NOT NULL,
            posicion INTEGER NOT NULL,
            simbolo TEXT NOT NULL,
            FOREIGN KEY (partida_id) REFERENCES partidas(id)
        )
    """)

    conexion.commit()
    conexion.close()
>>>>>>> c30926d43c46f40f7e0dfebe33f8d97fb319c235
