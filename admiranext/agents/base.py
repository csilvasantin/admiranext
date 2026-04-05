"""Clase base para todos los agentes del Consejo de Dirección."""

from __future__ import annotations

from typing import Optional

import anthropic

from admiranext.models import AgentResponse


# Synthesis structure per council side
SYNTHESIS_STRUCTURE = {
    "creativo": (
        "1. **Concepto central** (big idea)\n"
        "2. **Dirección de diseño**\n"
        "3. **Experiencia del usuario**\n"
        "4. **Narrativa y storytelling**\n"
        "5. **Plan de ejecución** (próximos pasos)"
    ),
    "racional": (
        "1. **Visión estratégica** (dirección y objetivos)\n"
        "2. **Viabilidad técnica** (tecnología y arquitectura)\n"
        "3. **Plan operativo** (ejecución y recursos)\n"
        "4. **Modelo financiero** (inversión, retorno y riesgos)\n"
        "5. **Próximos pasos** (roadmap priorizado)"
    ),
}


class CouncilAgent:
    """Agente base del Consejo de Dirección de AdmiraNext."""

    name: str = "Agente"
    role: str = "Miembro del Consejo"
    persona: str = ""
    category: str = ""
    side: str = "creativo"  # "creativo" or "racional"
    system_prompt: str = "Eres un miembro del consejo de dirección."
    model: str = "claude-sonnet-4-20250514"

    def __init__(self, client: Optional[anthropic.Anthropic] = None):
        self.client = client or anthropic.Anthropic()

    def respond(self, prompt: str, round_number: int = 1) -> AgentResponse:
        """Genera una respuesta del agente ante un prompt."""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        content = message.content[0].text
        return AgentResponse(
            agent_name=self.name,
            agent_role=self.role,
            content=content,
            round_number=round_number,
        )

    def propose(self, brief_text: str) -> AgentResponse:
        """Ronda 1: Propuesta individual ante el brief."""
        prompt = (
            f"Se te presenta el siguiente brief. "
            f"Da tu perspectiva profesional desde tu rol como {self.role}.\n\n"
            f"{brief_text}\n\n"
            f"Sé concreto, propositivo y aporta ideas accionables. "
            f"Máximo 300 palabras."
        )
        return self.respond(prompt, round_number=1)

    def debate(self, brief_text: str, other_proposals: list[AgentResponse]) -> AgentResponse:
        """Ronda 2: Debate — responde a las propuestas de los otros agentes."""
        others_text = "\n\n".join(
            f"**{p.agent_name} ({p.agent_role}):**\n{p.content}"
            for p in other_proposals
            if p.agent_name != self.name
        )
        prompt = (
            f"Brief original:\n{brief_text}\n\n"
            f"Estas son las propuestas de tus colegas del consejo:\n\n{others_text}\n\n"
            f"Como {self.role}, enriquece la discusión: "
            f"valida lo que te parece fuerte, cuestiona lo que creas débil, "
            f"y propón cómo integrar las ideas en una propuesta más potente. "
            f"Máximo 300 palabras."
        )
        return self.respond(prompt, round_number=2)

    def synthesize(self, brief_text: str, all_contributions: list[AgentResponse]) -> str:
        """Genera la síntesis final del consejo."""
        contributions_text = "\n\n".join(
            f"**{c.agent_name} ({c.agent_role}) — Ronda {c.round_number}:**\n{c.content}"
            for c in all_contributions
        )
        structure = SYNTHESIS_STRUCTURE.get(self.side, SYNTHESIS_STRUCTURE["creativo"])
        prompt = (
            f"Brief original:\n{brief_text}\n\n"
            f"A continuación están todas las contribuciones del consejo "
            f"(propuestas iniciales y debate):\n\n{contributions_text}\n\n"
            f"Como líder del Consejo, genera la PROPUESTA FINAL UNIFICADA. "
            f"Integra las mejores ideas de cada miembro en una propuesta coherente, "
            f"ambiciosa y ejecutable. Estructura tu respuesta con:\n"
            f"{structure}\n\n"
            f"Máximo 500 palabras."
        )
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text
