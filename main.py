#!/usr/bin/env python3
"""CLI del Consejo de Dirección — AdmiraNext."""

import os

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from admiranext.brainstorming import generate_brainstorming
from admiranext.council import Council, GROUPS
from admiranext.models import Brief
from admiranext.orgchart import generate_orgchart

load_dotenv(override=True)

console = Console()

AGENT_COLORS = {
    # Creativo
    "CCO": "bold red",
    "CDO": "bold blue",
    "CXO": "bold green",
    "CSO": "bold magenta",
    # Racional
    "CEO": "bold yellow",
    "CTO": "bold blue",
    "COO": "bold green",
    "CFO": "bold cyan",
}

BANNERS = {
    "leyendas": """
╔═══════════════════════════════════════════════════════════════╗
║        AdmiraNext — Consejo de Dirección  ⭐ Leyendas        ║
╠═══════════════════════════╦═══════════════════════════════════╣
║  🧠 RACIONAL (🔴 rojas)   ║  🎨 CREATIVO (🔵 azules)          ║
║  🏛️  CEO Steve Jobs       ║  💡 CCO Walt Disney               ║
║  ⚙️  CTO Steve Wozniak    ║  🎨 CDO Dieter Rams               ║
║  📋 COO Tim Cook          ║  🧭 CXO Howard Schultz            ║
║  💰 CFO Warren Buffett    ║  📖 CSO George Lucas               ║
╚═══════════════════════════╩═══════════════════════════════════╝
""",
    "coetaneos": """
╔═══════════════════════════════════════════════════════════════╗
║        AdmiraNext — Consejo de Dirección  🚀 Coetáneos       ║
╠═══════════════════════════╦═══════════════════════════════════╣
║  🧠 RACIONAL (🔴 rojas)   ║  🎨 CREATIVO (🔵 azules)          ║
║  🏛️  CEO Elon Musk        ║  💡 CCO John Lasseter             ║
║  ⚙️  CTO Jensen Huang     ║  🎨 CDO Jony Ive                  ║
║  📋 COO Gwynne Shotwell   ║  🧭 CXO Carlos Ratti              ║
║  💰 CFO Ruth Porat        ║  📖 CSO Ryan Reynolds              ║
╚═══════════════════════════╩═══════════════════════════════════╝
""",
}


def select_council() -> str:
    """Permite al usuario elegir el consejo y grupo."""
    console.print(
        Panel(
            "[bold]Elige la generación del Consejo:[/bold]\n\n"
            "  [yellow]1.[/yellow] ⭐ [bold]Leyendas[/bold]\n"
            "     🧠 Jobs · Wozniak · Cook · Buffett  ·  🎨 Disney · Rams · Schultz · Lucas\n\n"
            "  [yellow]2.[/yellow] 🚀 [bold]Coetáneos[/bold]\n"
            "     🧠 Musk · Huang · Shotwell · Porat  ·  🎨 Lasseter · Ive · Ratti · Reynolds",
            title="[bold]AdmiraNext — Consejo de Dirección[/bold]",
            border_style="cyan",
        )
    )
    mapping = {
        "1": "leyendas",
        "2": "coetaneos",
    }
    while True:
        choice = console.input("\n[bold cyan]Consejo (1/2) > [/bold cyan]").strip()
        if choice in mapping:
            return mapping[choice]
        else:
            console.print("[dim]Escribe 1 o 2[/dim]")


def on_proposal(response):
    color = AGENT_COLORS.get(response.agent_name, "white")
    console.print(
        Panel(
            Markdown(response.content),
            title=f"[{color}]{response.agent_name} — {response.agent_role}[/{color}]",
            subtitle="Propuesta individual",
            border_style=color.replace("bold ", ""),
        )
    )


def on_debate(response):
    color = AGENT_COLORS.get(response.agent_name, "white")
    console.print(
        Panel(
            Markdown(response.content),
            title=f"[{color}]{response.agent_name} — {response.agent_role}[/{color}]",
            subtitle="Debate",
            border_style=color.replace("bold ", ""),
        )
    )


def on_synthesis(synthesis):
    console.print()
    console.print(
        Panel(
            Markdown(synthesis),
            title="[bold yellow]PROPUESTA FINAL DEL CONSEJO[/bold yellow]",
            subtitle="Síntesis del líder",
            border_style="yellow",
            padding=(1, 2),
        )
    )


def main():
    # Generar organigrama
    generate_orgchart()

    # Selección de consejo
    group = select_council()
    console.print(BANNERS[group], style="bold cyan")

    console.print(
        f"[dim]Consejo mixto: 8 miembros (4 racionales + 4 creativos)[/dim]\n"
    )
    console.print("[bold]Escribe tu brief[/bold] (o 'salir' para terminar):\n")

    while True:
        brief_text = console.input("[bold cyan]Brief > [/bold cyan]")

        if brief_text.strip().lower() in ("salir", "exit", "q"):
            console.print("\n[dim]Hasta la próxima sesión.[/dim]")
            break

        if not brief_text.strip():
            continue

        brief = Brief(content=brief_text.strip())
        council = Council(group=group)

        console.print("\n[bold]═══ RONDA 1: PROPUESTAS INDIVIDUALES ═══[/bold]\n")
        console.print("[dim]Los agentes están preparando sus propuestas...[/dim]\n")

        def on_proposal_with_header(response):
            on_proposal(response)

        def on_debate_with_header(response, _header_shown=[False]):
            if not _header_shown[0]:
                console.print("\n[bold]═══ RONDA 2: DEBATE ═══[/bold]\n")
                console.print("[dim]Los agentes debaten entre sí...[/dim]\n")
                _header_shown[0] = True
            on_debate(response)

        def on_synthesis_with_header(synthesis):
            console.print("\n[bold]═══ SÍNTESIS FINAL ═══[/bold]")
            on_synthesis(synthesis)

        output = council.run(
            brief=brief,
            on_proposal=on_proposal_with_header,
            on_debate=on_debate_with_header,
            on_synthesis=on_synthesis_with_header,
        )

        # Generar documento Brainstorming en HTML
        filepath = generate_brainstorming(output)
        console.print(
            f"\n[bold green]📄 Documento Brainstorming guardado en:[/bold green] "
            f"[link=file://{os.path.abspath(filepath)}]{filepath}[/link]"
        )

        console.print("\n[dim]─── Listo. Escribe otro brief o 'salir'. ───[/dim]\n")


if __name__ == "__main__":
    main()
