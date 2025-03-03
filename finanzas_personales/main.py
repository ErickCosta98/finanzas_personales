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

if __name__ == "__main__":
    asyncio.run(main())
