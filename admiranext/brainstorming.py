"""Generador del documento HTML Brainstorming."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

from admiranext.models import CouncilOutput


_CREATIVE_COLORS = {
    "CCO": {"bg": "#FF4444", "light": "#FFF0F0", "text": "#CC0000"},
    "CDO": {"bg": "#4488FF", "light": "#F0F4FF", "text": "#0044CC"},
    "CXO": {"bg": "#44BB44", "light": "#F0FFF0", "text": "#008800"},
    "CSO": {"bg": "#BB44BB", "light": "#FFF0FF", "text": "#880088"},
}

_RATIONAL_COLORS = {
    "CEO": {"bg": "#FF8C00", "light": "#FFF5E6", "text": "#CC7000"},
    "CTO": {"bg": "#4488FF", "light": "#F0F4FF", "text": "#0044CC"},
    "COO": {"bg": "#44BB44", "light": "#F0FFF0", "text": "#008800"},
    "CFO": {"bg": "#DAA520", "light": "#FFF8E7", "text": "#8B6914"},
}

AGENT_COLORS = {**_CREATIVE_COLORS, **_RATIONAL_COLORS}

_CREATIVE_ICONS = {
    "CCO": "💡",
    "CDO": "🎨",
    "CXO": "🧭",
    "CSO": "📖",
}

_RATIONAL_ICONS = {
    "CEO": "🏛️",
    "CTO": "⚙️",
    "COO": "📋",
    "CFO": "💰",
}

AGENT_ICONS = {**_CREATIVE_ICONS, **_RATIONAL_ICONS}

AGENT_PERSONAS = {
    "creativo_leyendas": {
        "CCO": {"name": "Walt Disney", "category": "Leyenda"},
        "CDO": {"name": "Dieter Rams", "category": "Leyenda"},
        "CXO": {"name": "Howard Schultz", "category": "Leyenda"},
        "CSO": {"name": "George Lucas", "category": "Leyenda"},
    },
    "creativo_coetaneos": {
        "CCO": {"name": "John Lasseter", "category": "Coetáneo"},
        "CDO": {"name": "Jony Ive", "category": "Coetáneo"},
        "CXO": {"name": "Es Devlin", "category": "Coetáneo"},
        "CSO": {"name": "Ryan Reynolds", "category": "Coetáneo"},
    },
    "racional_leyendas": {
        "CEO": {"name": "Steve Jobs", "category": "Leyenda"},
        "CTO": {"name": "Steve Wozniak", "category": "Leyenda"},
        "COO": {"name": "Tim Cook", "category": "Leyenda"},
        "CFO": {"name": "Warren Buffett", "category": "Leyenda"},
    },
    "racional_coetaneos": {
        "CEO": {"name": "Elon Musk", "category": "Coetáneo"},
        "CTO": {"name": "Jensen Huang", "category": "Coetáneo"},
        "COO": {"name": "Gwynne Shotwell", "category": "Coetáneo"},
        "CFO": {"name": "Amy Hood", "category": "Coetáneo"},
    },
}

GROUP_LABELS = {
    "creativo_leyendas": "🎨 Creativo · ⭐ Leyendas",
    "creativo_coetaneos": "🎨 Creativo · 🚀 Coetáneos",
    "racional_leyendas": "🧠 Racional · ⭐ Leyendas",
    "racional_coetaneos": "🧠 Racional · 🚀 Coetáneos",
}


def generate_brainstorming(output: CouncilOutput, filepath: Optional[str] = None) -> str:
    """Genera un documento HTML con el resumen del brainstorming.

    Args:
        output: El resultado completo del consejo creativo.
        filepath: Ruta donde guardar el HTML. Si es None, usa output/.

    Returns:
        La ruta del archivo generado.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    date_display = now.strftime("%d de %B de %Y — %H:%M")

    if filepath is None:
        os.makedirs("output", exist_ok=True)
        filepath = f"output/brainstorming_{timestamp}.html"

    group = output.group
    personas = AGENT_PERSONAS.get(group, AGENT_PERSONAS["creativo_leyendas"])
    group_label = GROUP_LABELS.get(group, "🎨 Creativo · ⭐ Leyendas")
    brief_text = output.brief.content

    # Build agents bar dynamically from personas dict
    agents_bar_items = ""
    for role, persona_info in personas.items():
        icon = AGENT_ICONS.get(role, "🧠")
        agents_bar_items += f'<div class="agent-badge">{icon} {role} · {persona_info["name"]}</div>\n                '

    # Build proposal cards
    proposal_cards = ""
    for p in output.proposals:
        colors = AGENT_COLORS.get(p.agent_name, {"bg": "#666", "light": "#f5f5f5", "text": "#333"})
        icon = AGENT_ICONS.get(p.agent_name, "🧠")
        persona = personas.get(p.agent_name, {"name": "", "category": ""})
        content_html = _md_to_html(p.content)
        persona_html = f'<span class="agent-persona">{persona["name"]}</span>' if persona["name"] else ""
        category_badge = f'<span class="badge-category">{persona["category"]}</span>' if persona["category"] else ""
        proposal_cards += f"""
        <div class="card" style="border-left: 4px solid {colors['bg']};">
            <div class="card-header" style="background: {colors['light']};">
                <span class="agent-icon">{icon}</span>
                <div>
                    <span class="agent-name" style="color: {colors['text']};">{p.agent_name} <span class="agent-role-inline">· {p.agent_role}</span></span>
                    {persona_html}
                </div>
                {category_badge}
            </div>
            <div class="card-body">{content_html}</div>
        </div>
        """

    # Build debate cards
    debate_cards = ""
    for d in output.debate:
        colors = AGENT_COLORS.get(d.agent_name, {"bg": "#666", "light": "#f5f5f5", "text": "#333"})
        icon = AGENT_ICONS.get(d.agent_name, "🧠")
        persona = personas.get(d.agent_name, {"name": "", "category": ""})
        content_html = _md_to_html(d.content)
        persona_html = f'<span class="agent-persona">{persona["name"]}</span>' if persona["name"] else ""
        debate_cards += f"""
        <div class="card debate-card" style="border-left: 4px solid {colors['bg']};">
            <div class="card-header" style="background: {colors['light']};">
                <span class="agent-icon">{icon}</span>
                <div>
                    <span class="agent-name" style="color: {colors['text']};">{d.agent_name} <span class="agent-role-inline">· {d.agent_role}</span></span>
                    {persona_html}
                </div>
                <span class="badge-debate">Debate</span>
            </div>
            <div class="card-body">{content_html}</div>
        </div>
        """

    # Synthesis
    synthesis_html = _md_to_html(output.synthesis) if output.synthesis else "<p><em>Sin síntesis disponible.</em></p>"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brainstorming — Consejo Creativo</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Header Image */
        .header-image {{
            border-radius: 16px 16px 0 0;
            overflow: hidden;
            margin-bottom: 0;
        }}

        .header-image img {{
            width: 100%;
            height: auto;
            display: block;
            image-rendering: pixelated;
        }}

        /* Header */
        .header {{
            border-radius: 0 0 16px 16px;
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            border-radius: 16px;
            margin-bottom: 2rem;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }}

        .header .subtitle {{
            font-size: 1.1rem;
            opacity: 0.8;
        }}

        .header .date {{
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.6;
        }}

        .agents-bar {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }}

        .agent-badge {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(255,255,255,0.15);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
        }}

        /* Brief */
        .brief-section {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-left: 4px solid #f0ad4e;
        }}

        .brief-section h2 {{
            color: #f0ad4e;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }}

        .brief-section .brief-text {{
            font-size: 1.15rem;
            font-style: italic;
            color: #555;
        }}

        /* Section titles */
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin: 2.5rem 0 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #eee;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .section-number {{
            background: #1a1a2e;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            flex-shrink: 0;
        }}

        /* Cards */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 1.5rem;
        }}

        .card {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}

        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}

        .card-header {{
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .agent-icon {{
            font-size: 1.5rem;
        }}

        .agent-name {{
            font-weight: 700;
            font-size: 1.1rem;
            display: block;
        }}

        .agent-role {{
            font-size: 0.8rem;
            color: #888;
        }}

        .agent-role-inline {{
            font-weight: 400;
            font-size: 0.85rem;
            opacity: 0.7;
        }}

        .agent-persona {{
            display: block;
            font-size: 0.8rem;
            color: #666;
            font-style: italic;
        }}

        .badge-category {{
            margin-left: auto;
            background: linear-gradient(135deg, #f0ad4e, #ec971f);
            color: white;
            padding: 0.2rem 0.7rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .category-label {{
            margin-top: 1rem;
            font-size: 0.85rem;
            opacity: 0.7;
            letter-spacing: 1px;
        }}

        .badge-debate {{
            margin-left: auto;
            background: rgba(0,0,0,0.08);
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .card-body {{
            padding: 1.25rem 1.5rem;
            font-size: 0.95rem;
        }}

        .card-body p {{ margin-bottom: 0.75rem; }}
        .card-body ul, .card-body ol {{ margin: 0.5rem 0 0.75rem 1.5rem; }}
        .card-body li {{ margin-bottom: 0.3rem; }}
        .card-body strong {{ color: #222; }}
        .card-body h3 {{ margin: 1rem 0 0.5rem; font-size: 1.05rem; }}

        /* Synthesis */
        .synthesis {{
            background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
            border: 2px solid #f0ad4e;
            border-radius: 16px;
            padding: 2.5rem;
            margin-top: 2rem;
        }}

        .synthesis h2 {{
            color: #c87f0a;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }}

        .synthesis .content {{
            font-size: 1rem;
            line-height: 1.8;
        }}

        .synthesis .content p {{ margin-bottom: 0.75rem; }}
        .synthesis .content ul, .synthesis .content ol {{ margin: 0.5rem 0 0.75rem 1.5rem; }}
        .synthesis .content li {{ margin-bottom: 0.4rem; }}
        .synthesis .content strong {{ color: #8a5a00; }}
        .synthesis .content h3 {{ margin: 1.25rem 0 0.5rem; color: #8a5a00; }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color: #aaa;
            font-size: 0.85rem;
        }}

        @media (max-width: 600px) {{
            .container {{ padding: 1rem; }}
            .header h1 {{ font-size: 1.8rem; }}
            .cards-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header-image">
            <img src="assets/council-header.jpg" alt="Consejo Creativo AdmiraNext — Pixel Art">
        </div>
        <div class="header">
            <h1>🧠 Brainstorming</h1>
            <div class="subtitle">Consejo Creativo — AdmiraNext</div>
            <div class="agents-bar">
                {agents_bar_items}
            </div>
            <div class="category-label">{group_label}</div>
            <div class="date">{date_display}</div>
        </div>

        <div class="brief-section">
            <h2>📋 Brief Creativo</h2>
            <div class="brief-text">{brief_text}</div>
        </div>

        <div class="section-title">
            <span class="section-number">1</span>
            Propuestas Individuales
        </div>
        <div class="cards-grid">
            {proposal_cards}
        </div>

        <div class="section-title">
            <span class="section-number">2</span>
            Debate del Consejo
        </div>
        <div class="cards-grid">
            {debate_cards}
        </div>

        <div class="section-title">
            <span class="section-number">3</span>
            Propuesta Final Unificada
        </div>
        <div class="synthesis">
            <h2>⭐ Síntesis del Consejo Creativo</h2>
            <div class="content">{synthesis_html}</div>
        </div>

        <div class="footer">
            Generado por el Consejo Creativo — AdmiraNext v0.1.0
        </div>
    </div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


def _md_to_html(text: str) -> str:
    """Convierte markdown básico a HTML (sin dependencias externas)."""
    import re

    lines = text.split("\n")
    html_lines = []
    in_list = False
    list_type = None  # 'ul' or 'ol'

    for line in lines:
        stripped = line.strip()

        # Empty line
        if not stripped:
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
                list_type = None
            html_lines.append("")
            continue

        # Headers
        if stripped.startswith("### "):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            html_lines.append(f"<h3>{_inline_md(stripped[4:])}</h3>")
            continue
        if stripped.startswith("## "):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            html_lines.append(f"<h3>{_inline_md(stripped[3:])}</h3>")
            continue

        # Ordered list
        ol_match = re.match(r"^(\d+)[\.\)]\s+(.+)", stripped)
        if ol_match:
            if not in_list or list_type != "ol":
                if in_list:
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ol>")
                in_list = True
                list_type = "ol"
            html_lines.append(f"<li>{_inline_md(ol_match.group(2))}</li>")
            continue

        # Unordered list
        if stripped.startswith(("- ", "• ", "* ")):
            if not in_list or list_type != "ul":
                if in_list:
                    html_lines.append(f"</{list_type}>")
                html_lines.append("<ul>")
                in_list = True
                list_type = "ul"
            html_lines.append(f"<li>{_inline_md(stripped[2:])}</li>")
            continue

        # Regular paragraph
        if in_list:
            html_lines.append(f"</{list_type}>")
            in_list = False
            list_type = None
        html_lines.append(f"<p>{_inline_md(stripped)}</p>")

    if in_list:
        html_lines.append(f"</{list_type}>")

    return "\n".join(html_lines)


def _inline_md(text: str) -> str:
    """Convierte markdown inline (bold, italic, code) a HTML."""
    import re
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Quoted strings
    text = re.sub(r'"([^"]+)"', r'&ldquo;\1&rdquo;', text)
    return text
