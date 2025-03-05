# finanzas_personales/main.py
import asyncio
from finanzas_personales.database import Database
from finanzas_personales.interface import Interface

async def main():
    db = Database()
    try:
        interface = Interface(db)
        await interface.menu_principal()
    except KeyboardInterrupt:
        print("[yellow]Programa terminado por el usuario[/yellow]")
    finally:
        db.close()

def run_main():
    """Función síncrona que ejecuta la corrutina main."""
    asyncio.run(main())

if __name__ == "__main__":
    run_main()
