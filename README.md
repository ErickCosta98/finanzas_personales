[![PyPI Latest Release](https://img.shields.io/pypi/v/finanzas-personales.svg)](https://pypi.org/project/finanzas-personales/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/finanzas-personales)](https://pypi.org/project/finanzas-personales/)
[![GitHub Release Date](https://img.shields.io/github/release-date/ErickCosta98/finanzas_personales)](https://github.com/ErickCosta98/finanzas_personales/releases) [![GitHub License](https://img.shields.io/github/license/ErickCosta98/finanzas_personales)](https://github.com/ErickCosta98/financieros/blob/main/LICENSE)

# Finanzas Personales

Una aplicación de consola para gestionar finanzas personales, incluyendo ingresos, egresos, resúmenes y gráficos.

## Características

- Registro de ingresos y egresos con categorías predefinidas.
- Visualización de resúmenes financieros totales y mensuales.
- Gráficos en consola y generados como imágenes PNG.
- Interfaz interactiva con navegación por teclado.

## Requisitos

- Python 3.8+
- Dependencias: `rich`, `prompt_toolkit`, `matplotlib`

## Instalación

### Opción 1: Desde PyPI

1. Instala el paquete directamente desde PyPI:

   ```bash
   pip install finanzas_personales
   ```

2. Ejecuta la aplicación:

   ```bash
   finanzas_personales
   ```

### Opción 2: Clonar Repo

1. Clona el repositorio:

   ```bash
   git clone https://github.com/ErickCosta98/finanzas_personales.git
   cd finanzas_personales
   ```

2. Crear un entorno virtual (opcional, ver instrucciones por sistema operativo abajo).

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   python3 -m finanzas_personales.main
   ```

## Uso con Entorno Virtual

A continuación, se detallan los comandos para crear y activar un entorno virtual según el sistema operativo y la terminal utilizada.

### Linux / macOS

#### Bash

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Desactivar (cuando termines)
deactivate
```

#### Zsh

```zsh
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Desactivar
deactivate
```

#### Fish

```fish
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate.fish

# Desactivar
deactivate
```

### Windows

#### CMD

```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate.bat

# Desactivar
deactivate
```

#### PowerShell

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Desactivar
deactivate
```

#### Git Bash

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/Scripts/activate

# Desactivar
deactivate
```

## Uso General

- Usa las flechas ↑/↓ para navegar por los menús.
- Presiona Enter para seleccionar una opción.
- Ingresa datos como cantidad y descripción cuando se solicite.
- Usa Escape para salir de submenús o cerrar el programa.

## Captura de Pantalla

![Menú Principal](https://raw.githubusercontent.com/ErickCosta98/finanzas_personales/main/menu_principal.png)

## Estructura del Proyecto

- `database.py`: Manejo de la base de datos SQLite.
- `graphics.py`: Generación de gráficos en consola y PNG.
- `interface.py`: Lógica de la interfaz de usuario.
- `models.py`: Definición de categorías y estructuras de datos.
- `main.py`: Punto de entrada principal.

## Contribuir

¡Las contribuciones son bienvenidas! Por favor, abre un issue o un pull request.

## Licencia

MIT
