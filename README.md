# Tres en Raya

## Descripción

Este proyecto consiste en un juego de Tres en Raya desarrollado como parte del Proyecto Integrador Anual. El objetivo es permitir jugar partidas, registrar las jugadas y guardar la información en una base de datos.

## Tecnologías utilizadas

- Python
- FastAPI para la API REST
- SQLite para almacenar las partidas y las jugadas
- Pydantic para validar los datos
- HTML, CSS y JavaScript para la interfaz web

## Archivos principales

- `main.py`: define los endpoints de la API.
- `database.py`: administra la conexión y la creación de las tablas.
- `schemas.py`: valida los datos recibidos.
- `juego.py`: contiene la lógica del juego mediante una clase.
- `jugar.py`: permite ejecutar una versión por consola.
- `index.html`: contiene la interfaz web.

## Instalación

Se necesita Python 3.13 o una versión compatible.

Instalar las dependencias con:

```bash
py -3.13 -m pip install fastapi uvicorn
```

## Cómo ejecutar

1. Abrir una terminal en la carpeta del proyecto.
2. Iniciar la API:

```bash
py -3.13 -m uvicorn main:app --reload
```

3. Abrir una segunda terminal en la misma carpeta e iniciar el servidor web:

```bash
py -3.13 -m http.server 5500
```

4. Abrir `http://127.0.0.1:5500/index.html` en el navegador.
5. La documentación interactiva de la API está disponible en `http://127.0.0.1:8000/docs`.

## Base de datos

La aplicación utiliza SQLite. Las tablas se crean automáticamente al iniciar el backend.

## Estado del proyecto

Proyecto académico en desarrollo.
