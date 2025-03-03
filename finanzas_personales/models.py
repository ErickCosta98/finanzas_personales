# finanzas_personales/models.py
from typing import List, Dict

class FinanzasConfig:
    CATEGORIAS_INGRESOS: List[str] = ["Salario", "Freelance", "Inversiones", "Regalos/Bonos", "Otro"]
    CATEGORIAS_EGRESOS: List[str] = [
        "Vivienda", "Transporte", "Alimentación", "Servicios", 
        "Entretenimiento", "Salud", "Educación", "Ropa", "Ahorro/Inversiones", "Otro"
    ]
