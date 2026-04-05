"""Generador del Organigrama HTML de AdmiraNext."""

import os


COUNCIL_DATA = {
    "creativo": {
        "title": "Consejo Creativo",
        "icon": "🎨",
        "machine": "MacBookAirBlanco",
        "color": "#e74c3c",
        "roles": {
            "CCO": {
                "title": "Chief Creative Officer",
                "icon": "💡",
                "leyenda": {"name": "Walt Disney", "years": "1901-1966"},
                "coetaneo": {"name": "John Lasseter", "years": "1957-"},
            },
            "CDO": {
                "title": "Chief Design Officer",
                "icon": "🎨",
                "leyenda": {"name": "Dieter Rams", "years": "1932-"},
                "coetaneo": {"name": "Jony Ive", "years": "1967-"},
            },
            "CXO": {
                "title": "Chief Experience Officer",
                "icon": "🧭",
                "leyenda": {"name": "Howard Schultz", "years": "1953-"},
                "coetaneo": {"name": "Es Devlin", "years": "1971-"},
            },
            "CSO": {
                "title": "Chief Storytelling Officer",
                "icon": "📖",
                "leyenda": {"name": "George Lucas", "years": "1944-"},
                "coetaneo": {"name": "Ryan Reynolds", "years": "1976-"},
            },
        },
    },
    "racional": {
        "title": "Consejo Racional",
        "icon": "🧠",
        "machine": "MacBookAir16",
        "color": "#2980b9",
        "roles": {
            "CEO": {
                "title": "Chief Executive Officer",
                "icon": "🏛️",
                "leyenda": {"name": "Steve Jobs", "years": "1955-2011"},
                "coetaneo": {"name": "Elon Musk", "years": "1971-"},
            },
            "CTO": {
                "title": "Chief Technology Officer",
                "icon": "⚙️",
                "leyenda": {"name": "Steve Wozniak", "years": "1950-"},
                "coetaneo": {"name": "Jensen Huang", "years": "1963-"},
            },
            "COO": {
                "title": "Chief Operations Officer",
                "icon": "📋",
                "leyenda": {"name": "Tim Cook", "years": "1960-"},
                "coetaneo": {"name": "Gwynne Shotwell", "years": "1963-"},
            },
            "CFO": {
                "title": "Chief Financial Officer",
                "icon": "💰",
                "leyenda": {"name": "Warren Buffett", "years": "1930-"},
                "coetaneo": {"name": "Amy Hood", "years": "1972-"},
            },
        },
    },
}


def generate_orgchart(filepath="orgchart.html"):
    """Genera el organigrama HTML completo de AdmiraNext."""

    # Build role cards for each side
    def build_side(side_key):
        side = COUNCIL_DATA[side_key]
        cards = ""
        for role_key, role_data in side.items() if isinstance(side, dict) else []:
            pass

        role_cards = ""
        for role_key, role_data in side["roles"].items():
            role_cards += f"""
            <div class="role-card">
                <div class="role-header">
                    <span class="role-icon">{role_data['icon']}</span>
                    <div>
                        <span class="role-code">{role_key}</span>
                        <span class="role-title">{role_data['title']}</span>
                    </div>
                </div>
                <div class="personas-row">
                    <div class="persona leyenda">
                        <span class="persona-badge">⭐ Leyenda</span>
                        <span class="persona-name">{role_data['leyenda']['name']}</span>
                        <span class="persona-years">{role_data['leyenda']['years']}</span>
                    </div>
                    <div class="persona coetaneo">
                        <span class="persona-badge">🚀 Coetáneo</span>
                        <span class="persona-name">{role_data['coetaneo']['name']}</span>
                        <span class="persona-years">{role_data['coetaneo']['years']}</span>
                    </div>
                </div>
            </div>
            """
        return role_cards

    creativo_cards = build_side("creativo")
    racional_cards = build_side("racional")

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Organigrama — AdmiraNext</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}

        /* Header */
        .org-header {{
            text-align: center;
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        .org-header img {{
            width: 100%;
            max-width: 800px;
            border-radius: 12px;
            image-rendering: pixelated;
            margin-bottom: 1.5rem;
        }}
        .org-header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, #e74c3c, #3498db);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .org-header .subtitle {{
            color: #888;
            font-size: 1.1rem;
        }}

        /* Council grid */
        .councils {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }}

        .council-side {{
            background: #1a1a2e;
            border-radius: 16px;
            padding: 1.5rem;
            border-top: 4px solid;
        }}
        .council-side.creativo {{ border-color: #e74c3c; }}
        .council-side.racional {{ border-color: #3498db; }}

        .side-header {{
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #2a2a3e;
        }}
        .side-header h2 {{
            font-size: 1.4rem;
            margin-bottom: 0.3rem;
        }}
        .side-header .machine {{
            font-size: 0.8rem;
            color: #666;
            background: #0f0f1a;
            padding: 0.2rem 0.6rem;
            border-radius: 8px;
            display: inline-block;
            margin-top: 0.4rem;
        }}

        /* Role cards */
        .role-card {{
            background: #16213e;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        .role-header {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.8rem;
        }}
        .role-icon {{ font-size: 1.3rem; }}
        .role-code {{
            font-weight: 800;
            font-size: 1rem;
            display: block;
        }}
        .role-title {{
            font-size: 0.75rem;
            color: #888;
        }}

        .personas-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
        }}
        .persona {{
            background: #0f0f1a;
            border-radius: 8px;
            padding: 0.6rem;
            text-align: center;
        }}
        .persona-badge {{
            display: block;
            font-size: 0.65rem;
            margin-bottom: 0.3rem;
            opacity: 0.7;
        }}
        .persona-name {{
            display: block;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .persona-years {{
            display: block;
            font-size: 0.7rem;
            color: #555;
            margin-top: 0.1rem;
        }}

        /* Connector line */
        .connector {{
            text-align: center;
            margin: 1.5rem 0;
            font-size: 1.5rem;
            color: #333;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #444;
            font-size: 0.8rem;
        }}

        @media (max-width: 768px) {{
            .councils {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="org-header">
            <img src="assets/council-header.jpg" alt="AdmiraNext Council">
            <h1>AdmiraNext</h1>
            <div class="subtitle">Consejo de Dirección — Organigrama</div>
        </div>

        <div class="councils">
            <div class="council-side creativo">
                <div class="side-header">
                    <h2>🎨 Consejo Creativo</h2>
                    <div class="machine">💻 MacBookAirBlanco</div>
                </div>
                {creativo_cards}
            </div>

            <div class="council-side racional">
                <div class="side-header">
                    <h2>🧠 Consejo Racional</h2>
                    <div class="machine">🌐 MacBookAir16</div>
                </div>
                {racional_cards}
            </div>
        </div>

        <div class="footer">
            AdmiraNext v0.2.0 — Consejo de Dirección con 16 agentes IA
        </div>
    </div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return filepath


if __name__ == "__main__":
    path = generate_orgchart()
    print(f"Organigrama generado: {path}")
