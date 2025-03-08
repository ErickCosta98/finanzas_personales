# finanzas_personales/interface.py
import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout as PromptLayout
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.validation import Validator
from typing import List, Dict, Tuple
from .database import Database
from .graphics import GraficaConsola, crear_grafico_categorias
from .models import FinanzasConfig
from .clearConsole import clear_console

console = Console()

class NumberValidator(Validator):
    """Validador para asegurar que la entrada sea un número no negativo."""
    def validate(self, document):
        text = document.text
        try:
            value = float(text)
            if value < 0:
                raise ValueError("La cantidad no puede ser negativa")
        except ValueError:
            raise ValueError("Por favor, ingrese un número válido")

class Interface:
    def __init__(self, db: Database):
        self.db = db
        self.opciones_principal = [
            "Registrar Ingreso", "Registrar Egreso", "Ver Transacciones",
            "Ver Resumen", "Gráficos", "Salir"
        ]
        self.opciones_graficos = [
            "Ingresos (Consola)", "Egresos (Consola)", "Ingresos (Imagen)",
            "Egresos (Imagen)", "Volver"
        ]

    def preparar_dashboard(self, opcion_seleccionada: int = 0) -> Tuple[List[str], FormattedText, Layout]:
        """Prepara los datos del dashboard sin imprimirlo."""
        resumen_total = self.db.obtener_resumen()
        resumen_mes = self.db.obtener_resumen_mes_actual()
        ingresos_por_categoria = self.db.obtener_datos_por_categoria("Ingreso", "mes")
        egresos_por_categoria = self.db.obtener_datos_por_categoria("Egreso", "mes")
        transacciones_recientes = self.db.obtener_transacciones(5)

        layout = Layout()
        layout.split_column(Layout(name="header"), Layout(name="body", ratio=3))
        layout["body"].split_row(Layout(name="left"), Layout(name="right", ratio=2))
        layout["right"].split_column(Layout(name="top_right"), Layout(name="bottom_right"))

        tabla_resumen = Table(box=box.MINIMAL, expand=True)
        tabla_resumen.add_column("Concepto", style="bright_cyan")
        tabla_resumen.add_column("Mes Actual", justify="right", style="white")
        tabla_resumen.add_column("Total", justify="right", style="white")
        
        tabla_resumen.add_row("Ingresos", f"[green]${resumen_mes['ingresos']:,.2f}[/green]", 
                            f"[green]${resumen_total['ingresos']:,.2f}[/green]")
        tabla_resumen.add_row("Egresos", f"[red]${resumen_mes['egresos']:,.2f}[/red]", 
                            f"[red]${resumen_total['egresos']:,.2f}[/red]")
        color_mes = "green" if resumen_mes['balance'] >= 0 else "red"
        color_total = "green" if resumen_total['balance'] >= 0 else "red"
        tabla_resumen.add_row("Balance", f"[{color_mes}]${resumen_mes['balance']:,.2f}[/{color_mes}]", 
                            f"[{color_total}]${resumen_total['balance']:,.2f}[/{color_total}]")

        tabla_transacciones = Table(title="Transacciones Recientes", box=box.MINIMAL, expand=True)
        tabla_transacciones.add_column("Fecha", style="bright_cyan")
        tabla_transacciones.add_column("Tipo", style="white")
        tabla_transacciones.add_column("Categoría", style="white")
        tabla_transacciones.add_column("Monto", justify="right", style="white")
        
        for t in transacciones_recientes:
            tipo_color = "green" if t["tipo"] == "Ingreso" else "red"
            tabla_transacciones.add_row(t["fecha"], f"[{tipo_color}]{t['tipo']}[/{tipo_color}]", 
                                      t["categoria"], f"${t['cantidad']:,.2f}")

        grafico_ingresos = GraficaConsola.pie_ascii(ingresos_por_categoria, f"Ingresos ({resumen_mes['mes']})")
        grafico_egresos = GraficaConsola.barra_horizontal(egresos_por_categoria, f"Egresos ({resumen_mes['mes']})")

        layout["header"].update(Panel(tabla_resumen, title=f"Resumen - {resumen_mes['mes']}", box=box.MINIMAL))
        layout["left"].update(grafico_ingresos)
        layout["top_right"].update(grafico_egresos)
        layout["bottom_right"].update(tabla_transacciones)
        
        menu_text = [("white bold", "Menú:\n")]
        for i, opcion in enumerate(self.opciones_principal):
            if i == opcion_seleccionada:
                menu_text.append(("yellow bold", f"→ {opcion}\n"))
            else:
                menu_text.append(("white", f"  {opcion}\n"))
        
        return self.opciones_principal, FormattedText(menu_text), layout

    async def seleccionar_categoria(self, categorias: List[str], tipo: str) -> str:
        clear_console()
        color = "green" if tipo == "Ingreso" else "red"
        console.print(Panel(f"[bold][{color}]REGISTRAR {tipo.upper()}[/{color}][/bold]", box=box.ROUNDED))
        indice = [0]
        
        def get_menu_text():
            menu_text = []
            for i, cat in enumerate(categorias):
                if i == indice[0]:
                    menu_text.append(("yellow bold", f"→ {cat}\n"))
                else:
                    menu_text.append(("white", f"  {cat}\n"))
            return FormattedText(menu_text)

        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        def _(event):
            if indice[0] > 0:
                indice[0] -= 1
                app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        @bindings.add(Keys.Down)
        def _(event):
            if indice[0] < len(categorias) - 1:
                indice[0] += 1
                app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        @bindings.add(Keys.Enter)
        def _(event):
            event.app.exit(result=categorias[indice[0]])

        @bindings.add(Keys.Escape)
        def _(event):
            event.app.exit(result=None)

        app = Application(
            layout=PromptLayout(Window(content=FormattedTextControl(get_menu_text()))),
            key_bindings=bindings,
            full_screen=False
        )
        return await app.run_async()

    async def menu_ingreso(self):
        categoria = await self.seleccionar_categoria(FinanzasConfig.CATEGORIAS_INGRESOS, "Ingreso")
        if not categoria:
            return
        
        cantidad_session = PromptSession("Cantidad: ", validator=NumberValidator(), validate_while_typing=False)
        cantidad = float(await cantidad_session.prompt_async())

        descripcion_session = PromptSession("Descripción: ")
        descripcion = await descripcion_session.prompt_async()

        confirm_session = PromptSession(f"¿Confirmar ingreso de ${cantidad:,.2f} en '{categoria}'? (s/n): ")
        confirm = (await confirm_session.prompt_async()).lower()
        if confirm in ('s', 'si', 'y', 'yes'):
            self.db.agregar_transaccion("Ingreso", categoria, cantidad, descripcion)

    async def menu_egreso(self):
        categoria = await self.seleccionar_categoria(FinanzasConfig.CATEGORIAS_EGRESOS, "Egreso")
        if not categoria:
            return
        
        cantidad_session = PromptSession("Cantidad: ", validator=NumberValidator(), validate_while_typing=False)
        cantidad = float(await cantidad_session.prompt_async())

        descripcion_session = PromptSession("Descripción: ")
        descripcion = await descripcion_session.prompt_async()

        confirm_session = PromptSession(f"¿Confirmar egreso de ${cantidad:,.2f} en '{categoria}'? (s/n): ")
        confirm = (await confirm_session.prompt_async()).lower()
        if confirm in ('s', 'si', 'y', 'yes'):
            self.db.agregar_transaccion("Egreso", categoria, cantidad, descripcion)

    async def mostrar_transacciones(self):
        pagina = [0]
        items_por_pagina = 10
        while True:
            clear_console()
            transacciones = self.db.obtener_transacciones()
            if not transacciones:
                console.print("[yellow]No hay transacciones registradas.[/yellow]")
                await asyncio.sleep(2)
                return
                
            inicio = pagina[0] * items_por_pagina
            fin = min(inicio + items_por_pagina, len(transacciones))
            table = Table(title=f"Transacciones (Página {pagina[0] + 1}/{(len(transacciones) - 1) // items_por_pagina + 1})")
            table.add_column("Fecha", style="bright_cyan")
            table.add_column("Tipo", style="white")
            table.add_column("Categoría", style="white")
            table.add_column("Monto", justify="right", style="white")
            table.add_column("Descripción", style="white")
            
            for t in transacciones[inicio:fin]:
                tipo_color = "green" if t["tipo"] == "Ingreso" else "red"
                table.add_row(t["fecha"], f"[{tipo_color}]{t['tipo']}[/{tipo_color}]", 
                            t["categoria"], f"${t['cantidad']:,.2f}", t["descripcion"])
            
            console.print(table)
            console.print("\n[←] Anterior  [→] Siguiente  [Esc] Salir")
            
            bindings = KeyBindings()

            @bindings.add(Keys.Left)
            def _(event):
                if pagina[0] > 0:
                    pagina[0] -= 1
                    event.app.exit(result="update")

            @bindings.add(Keys.Right)
            def _(event):
                if fin < len(transacciones):
                    pagina[0] += 1
                    event.app.exit(result="update")

            @bindings.add(Keys.Escape)
            def _(event):
                event.app.exit(result="exit")

            session = PromptSession("", key_bindings=bindings)
            result = await session.prompt_async()
            if result == "exit":
                return
            elif result != "update":
                return

    async def mostrar_resumen(self):
        clear_console()
        resumen_total = self.db.obtener_resumen()
        resumen_mes = self.db.obtener_resumen_mes_actual()
        egresos_mes = self.db.obtener_datos_por_categoria("Egreso", "mes")
        
        layout = Layout()
        layout.split_row(Layout(name="resumen"), Layout(name="distribuciones"))
        
        tabla_resumen = Table(box=box.MINIMAL)
        tabla_resumen.add_column("Concepto", style="bright_cyan")
        tabla_resumen.add_column("Mes Actual", justify="right", style="white")
        tabla_resumen.add_column("Total", justify="right", style="white")
        
        tabla_resumen.add_row("Ingresos", f"[green]${resumen_mes['ingresos']:,.2f}[/green]", 
                            f"[green]${resumen_total['ingresos']:,.2f}[/green]")
        tabla_resumen.add_row("Egresos", f"[red]${resumen_mes['egresos']:,.2f}[/red]", 
                            f"[red]${resumen_total['egresos']:,.2f}[/red]")
        color_mes = "green" if resumen_mes['balance'] >= 0 else "red"
        color_total = "green" if resumen_total['balance'] >= 0 else "red"
        tabla_resumen.add_row("Balance", f"[{color_mes}]${resumen_mes['balance']:,.2f}[/{color_mes}]", 
                            f"[{color_total}]${resumen_total['balance']:,.2f}[/{color_total}]")
        
        tabla_distribucion = Table(box=box.MINIMAL)
        tabla_distribucion.add_column("Categoría", style="white")
        tabla_distribucion.add_column("Monto", justify="right", style="white")
        tabla_distribucion.add_column("%", justify="right", style="white")
        
        total_egresos = sum(egresos_mes.values()) or 1
        for cat, monto in sorted(egresos_mes.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (monto / total_egresos) * 100
            tabla_distribucion.add_row(cat, f"${monto:,.2f}", f"{porcentaje:.1f}%")
        
        layout["resumen"].update(Panel(tabla_resumen, title=f"Resumen - {resumen_mes['mes']}", box=box.MINIMAL))
        layout["distribuciones"].update(Panel(tabla_distribucion, title="Distribución Gastos", box=box.MINIMAL))
        
        console.print(layout)
        console.print("\n[Esc] Salir")
        
        bindings = KeyBindings()

        @bindings.add(Keys.Escape)
        def _(event):
            event.app.exit(result="exit")

        session = PromptSession("", key_bindings=bindings)
        await session.prompt_async()

    async def menu_graficos(self):
        indice = [0]
        
        def get_menu_text():
            menu_text = [("white bold", "Gráficos:\n")]
            for i, opt in enumerate(self.opciones_graficos):
                if i == indice[0]:
                    menu_text.append(("yellow bold", f"→ {opt}\n"))
                else:
                    menu_text.append(("white", f"  {opt}\n"))
            return FormattedText(menu_text)

        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        def _(event):
            if indice[0] > 0:
                indice[0] -= 1
                app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        @bindings.add(Keys.Down)
        def _(event):
            if indice[0] < len(self.opciones_graficos) - 1:
                indice[0] += 1
                app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        @bindings.add(Keys.Enter)
        def _(event):
            event.app.exit(result=indice[0])

        @bindings.add(Keys.Escape)
        def _(event):
            event.app.exit(result=None)

        app = Application(
            layout=PromptLayout(Window(content=FormattedTextControl(get_menu_text()))),
            key_bindings=bindings,
            full_screen=False
        )
        seleccion = await app.run_async()
        
        if seleccion is not None:
            if seleccion == 0:
                await self.mostrar_grafico_consola("Ingreso")
            elif seleccion == 1:
                await self.mostrar_grafico_consola("Egreso")
            elif seleccion == 2:
                crear_grafico_categorias("Ingreso", self.db.obtener_datos_por_categoria("Ingreso"))
            elif seleccion == 3:
                crear_grafico_categorias("Egreso", self.db.obtener_datos_por_categoria("Egreso"))

    async def mostrar_grafico_consola(self, tipo: str):
        clear_console()
        datos = self.db.obtener_datos_por_categoria(tipo)
        if not datos:
            console.print(f"[yellow]No hay datos de {tipo.lower()} para graficar.[/yellow]")
            await asyncio.sleep(2)
            return
            
        grafico = GraficaConsola.pie_ascii(datos, f"{tipo}s") if tipo == "Ingreso" else \
                 GraficaConsola.barra_horizontal(datos, f"{tipo}s")
        console.print(grafico)
        console.print("\n[Esc] Salir")
        
        bindings = KeyBindings()

        @bindings.add(Keys.Escape)
        def _(event):
            event.app.exit(result="exit")

        session = PromptSession("", key_bindings=bindings)
        await session.prompt_async()

    async def menu_principal(self):
        opcion_seleccionada = [0]
        opciones, menu_text_inicial, dashboard_layout = self.preparar_dashboard(opcion_seleccionada[0])
        
        # Imprimir el dashboard una vez al inicio
        console.print(Panel(
            Align.center("[bold bright_cyan]FINANZAS PERSONALES[/bold bright_cyan]", vertical="middle"),
            box=box.ROUNDED,
            border_style="bright_blue"
        ))
        console.print(dashboard_layout)

        def get_menu_text():
            # No volvemos a preparar el dashboard aquí, solo actualizamos el menú
            menu_text = [("white bold", "Menú:\n")]
            for i, opcion in enumerate(opciones):
                if i == opcion_seleccionada[0]:
                    menu_text.append(("yellow bold", f"→ {opcion}\n"))
                else:
                    menu_text.append(("white", f"  {opcion}\n"))
            return FormattedText(menu_text)

        bindings = KeyBindings()

        @bindings.add(Keys.Up)
        def _(event):
            if opcion_seleccionada[0] > 0:
                opcion_seleccionada[0] -= 1
                app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        @bindings.add(Keys.Down)
        def _(event):
            if opcion_seleccionada[0] < len(opciones) - 1:
                opcion_seleccionada[0] += 1
                app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        @bindings.add(Keys.Enter)
        async def _(event):
            if opcion_seleccionada[0] == 0:
                await self.menu_ingreso()
            elif opcion_seleccionada[0] == 1:
                await self.menu_egreso()
            elif opcion_seleccionada[0] == 2:
                await self.mostrar_transacciones()
            elif opcion_seleccionada[0] == 3:
                await self.mostrar_resumen()
            elif opcion_seleccionada[0] == 4:
                await self.menu_graficos()
            elif opcion_seleccionada[0] == 5:
                clear_console()
                console.print("[yellow]¡Hasta pronto![/yellow]")
                self.db.close()
                event.app.exit()
            # Refrescar el dashboard completo después de regresar de un submenú
            clear_console()
            console.print(Panel(
                Align.center("[bold bright_cyan]FINANZAS PERSONALES[/bold bright_cyan]", vertical="middle"),
                box=box.ROUNDED,
                border_style="bright_blue"
            ))
            _, _, new_dashboard = self.preparar_dashboard(opcion_seleccionada[0])
            console.print(new_dashboard)
            app.layout = PromptLayout(Window(content=FormattedTextControl(get_menu_text())))

        app = Application(
            layout=PromptLayout(Window(content=FormattedTextControl(get_menu_text()))),
            key_bindings=bindings,
            full_screen=False
        )
        await app.run_async()
