# proyecto-bases-de-datos

Proyecto para el curso CC3201

## Integrantes
 
- Nicolás Acevedo
- Catalina Parra
- Pablo Skewes

## Descripción
El proyecto consiste en una aplicación web que permite buscar recorridos de parques vehiculares en Chile. La aplicación permite ingresar un origen y un destino, y muestra los recorridos que cumplen con estos criterios. Además, se puede ver el recorrido en un mapa y se puede ver información de los vehículos que realizan el recorrido.

## Instalación

Para instalar las dependencias del proyecto, se recomienda utilizar un entorno virtual de python. Para esto, se debe ejecutar el siguiente comando en la carpeta raíz del proyecto:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e project_logger
```

Para que el backend funcione correctamente, se debe crear un archivo `.env` en la carpeta `backend` con completando la siguiente información (se puede copiar el archivo `.env.example`):

```
SISTEMA=""
USUARIO=""
PASSWORD=""
HOST=""
PUERTO=""
DB=""
```

## Ejecución
Para ejecutar el proyecto, se debe ejecutar el frontend y el backend por separado. Para esto, se deben ejecutar los siguientes comandos en la carpeta raíz del proyecto:

```bash
make run_backend
make run_frontend
```

Tras esto, se puede acceder al frontend en el puerto 8090 y al backend en el puerto 8091.

## Documentación
### Frontend
El frontend está desarrollado en Dash, una librería de Python para crear aplicaciones web.
La estructura del frontend es la siguiente:

```
frontend
├── app.py # Archivo principal del frontend
├── logs # Logs del frontend
├── data # Datos usados en la aplicación
│   ├──  regiones.json # Regiones de Chile en formato GeoJSON
├── src # Código fuente del frontend
│   ├── components # Componentes de Dash
│   │   ├── __init__.py
│   │   ├── layout.py # Layout de la aplicación
│   │   ├── chile_map.py # Componente del mapa de Chile
│   │   ├── buscador_recorrido.py # Componente del buscador de recorridos
│   ├── ids.py # Identificadores de los componentes
│   ├── logger.py # Logger del frontend
│   ├── __init__.py
```

### Backend
El backend está desarrollado con FastAPI y SQLAlchemy. La estructura del backend es la siguiente:

```
backend
├── main.py # Archivo principal del backend, también se encuentran las rutas
├── logs # Logs del backend
├── src # Código fuente del backend
│   ├── __init__.py
│   ├── database.py # Configuración/conexión de la base de datos
│   ├── models.py # Modelos de la base de datos (ORM)
│   ├── logger.py # Logger del backend
│   ├── schemas.py # Schemas de los modelos (Pydantic)
│   ├── crud.py # Funciones de acceso a la base de datos
│── __init__.py
|── .env # Archivo de configuración: contiene la información de la base de datos
```