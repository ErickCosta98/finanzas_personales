# finanzas_personales/database.py
import os
import sqlite3
from typing import List, Dict
import datetime
import calendar

class Database:
    def __init__(self, db_path: str = "~/finanzas_personales.db"):
        self.db_path = os.path.expanduser(db_path)
        self.conexion = None
        self.iniciar_bd()

    def iniciar_bd(self):
        try:
            self.conexion = sqlite3.connect(self.db_path)
            cursor = self.conexion.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                tipo TEXT,
                categoria TEXT,
                cantidad REAL,
                descripcion TEXT
            )
            ''')
            self.conexion.commit()
        except sqlite3.Error as e:
            print(f"[red]Error al inicializar la base de datos: {e}[/red]")
            raise SystemExit(1)

    def agregar_transaccion(self, tipo: str, categoria: str, cantidad: float, descripcion: str) -> None:
        try:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d")
            cursor = self.conexion.cursor()
            cursor.execute(
                "INSERT INTO transacciones (fecha, tipo, categoria, cantidad, descripcion) VALUES (?, ?, ?, ?, ?)",
                (fecha, tipo, categoria, cantidad, descripcion)
            )
            self.conexion.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error al agregar transacción: {e}")

    def obtener_transacciones(self, limite: int = None) -> List[Dict]:
        try:
            cursor = self.conexion.cursor()
            query = "SELECT * FROM transacciones ORDER BY fecha DESC"
            if limite:
                query += " LIMIT ?"
                cursor.execute(query, (limite,))
            else:
                cursor.execute(query)
            return [{"id": t[0], "fecha": t[1], "tipo": t[2], "categoria": t[3], 
                     "cantidad": t[4], "descripcion": t[5]} for t in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"[red]Error al obtener transacciones: {e}[/red]")
            return []

    def obtener_resumen(self) -> Dict:
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT SUM(cantidad) FROM transacciones WHERE tipo='Ingreso'")
            ingresos = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(cantidad) FROM transacciones WHERE tipo='Egreso'")
            egresos = cursor.fetchone()[0] or 0
            return {"ingresos": ingresos, "egresos": egresos, "balance": ingresos - egresos}
        except sqlite3.Error as e:
            print(f"[red]Error al obtener resumen: {e}[/red]")
            return {"ingresos": 0, "egresos": 0, "balance": 0}

    def obtener_resumen_mes_actual(self) -> Dict:
        try:
            hoy = datetime.datetime.now()
            inicio_mes = f"{hoy.year}-{hoy.month:02d}-01"
            ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
            fin_mes = f"{hoy.year}-{hoy.month:02d}-{ultimo_dia}"
            
            cursor = self.conexion.cursor()
            cursor.execute(
                "SELECT SUM(cantidad) FROM transacciones WHERE tipo='Ingreso' AND fecha BETWEEN ? AND ?",
                (inicio_mes, fin_mes)
            )
            ingresos = cursor.fetchone()[0] or 0
            cursor.execute(
                "SELECT SUM(cantidad) FROM transacciones WHERE tipo='Egreso' AND fecha BETWEEN ? AND ?",
                (inicio_mes, fin_mes)
            )
            egresos = cursor.fetchone()[0] or 0
            return {
                "mes": hoy.strftime("%B %Y"),
                "ingresos": ingresos,
                "egresos": egresos,
                "balance": ingresos - egresos
            }
        except sqlite3.Error as e:
            print(f"[red]Error al obtener resumen del mes: {e}[/red]")
            return {"mes": "", "ingresos": 0, "egresos": 0, "balance": 0}

    def obtener_datos_por_categoria(self, tipo: str, periodo: str = "total") -> Dict:
        try:
            cursor = self.conexion.cursor()
            consulta = "SELECT categoria, SUM(cantidad) FROM transacciones WHERE tipo=?"
            params = [tipo]
            
            if periodo == "mes":
                hoy = datetime.datetime.now()
                inicio_mes = f"{hoy.year}-{hoy.month:02d}-01"
                ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
                fin_mes = f"{hoy.year}-{hoy.month:02d}-{ultimo_dia}"
                consulta += " AND fecha BETWEEN ? AND ?"
                params.extend([inicio_mes, fin_mes])
            
            consulta += " GROUP BY categoria"
            cursor.execute(consulta, params)
            resultado = dict(cursor.fetchall())
            return resultado
        except sqlite3.Error as e:
            print(f"[red]Error al obtener datos por categoría: {e}[/red]")
            return {}

    def close(self):
        if self.conexion:
            self.conexion.close()
