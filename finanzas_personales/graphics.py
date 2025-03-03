# finanzas_personales/graphics.py
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich import box
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict
import datetime

console = Console()

class GraficaConsola:
    @staticmethod
    def barra_horizontal(datos: Dict, titulo: str, color_positivo: str = "green", color_negativo: str = "red"):
        if not datos:
            return Panel("[yellow]No hay datos disponibles[/yellow]", title=titulo)
            
        max_valor = max(abs(v) for v in datos.values()) or 1
        ancho_max = 40
        
        elementos = []
        for categoria, valor in datos.items():
            longitud = int((abs(valor) / max_valor) * ancho_max) or (1 if valor != 0 else 0)
            color = color_positivo if valor >= 0 else color_negativo
            barra = Text("█" * longitud, style=color)
            valor_texto = Text(f" ${abs(valor):,.2f}", style=f"bold {color}")
            categoria_texto = Text(f"{categoria:<15}", style="white")
            linea = Text.assemble(categoria_texto, " ", barra, " ", valor_texto)
            elementos.append(linea)
            
        return Panel(Group(*elementos), title=titulo, box=box.ROUNDED, border_style="bright_cyan")

    @staticmethod
    def pie_ascii(datos: Dict, titulo: str):
        if not datos:
            return Panel("[yellow]No hay datos disponibles[/yellow]", title=titulo)
        
        if not isinstance(datos, dict):
            console.print(f"[red]Error: 'datos' no es un diccionario, recibido: {type(datos)}[/red]")
            return Panel("[red]Error en datos[/red]", title=titulo)
            
        total = sum(datos.values()) or 1
        colores = ["bright_red", "bright_green", "bright_blue", "bright_yellow", "bright_magenta", "bright_cyan"]
        
        elementos = []
        try:
            for i, (categoria, valor) in enumerate(datos.items()):
                porcentaje = (valor / total) * 100
                color = colores[i % len(colores)]
                linea = Text.assemble(
                    Text("● ", style=color),
                    Text(f"{categoria:<15}", style="white"),
                    Text(f"${valor:,.2f}", style=color),
                    Text(f" ({porcentaje:.1f}%)", style="grey50")
                )
                elementos.append(linea)
            if not elementos:
                return Panel("[yellow]No hay elementos para mostrar[/yellow]", title=titulo)
            return Panel(Group(*elementos), title=titulo, box=box.ROUNDED, border_style="bright_cyan")
        except Exception as e:
            console.print(f"[red]Error al crear gráfico de pastel: {e}[/red]")
            return Panel("[red]Error al generar gráfico[/red]", title=titulo)

def crear_grafico_categorias(tipo: str, datos: Dict):
    """Genera y guarda un gráfico de pastel con matplotlib."""
    if not datos:
        console.print(f"[yellow]No hay datos de {tipo.lower()} para graficar.[/yellow]")
        time.sleep(2)
        return
        
    Path("graficos").mkdir(exist_ok=True)
    plt.figure(figsize=(10, 7))
    plt.pie(list(datos.values()), labels=list(datos.keys()), autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title(f'Distribución de {tipo}s por Categoría')
    filename = f"graficos/{tipo.lower()}_por_categoria_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    plt.close()
    console.print(f"[green]Gráfico guardado como '{filename}'[/green]")
    time.sleep(2)
