"""Modelos de datos para el Consejo de Dirección de AdmiraNext."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Brief:
    """Brief que se presenta al consejo."""

    content: str
    client: str = "Sin especificar"
    objective: str = "Sin especificar"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_prompt(self) -> str:
        parts = [f"## Brief\n\n{self.content}"]
        if self.client != "Sin especificar":
            parts.append(f"\n**Cliente:** {self.client}")
        if self.objective != "Sin especificar":
            parts.append(f"\n**Objetivo:** {self.objective}")
        return "\n".join(parts)


@dataclass
class AgentResponse:
    """Respuesta individual de un agente."""

    agent_name: str
    agent_role: str
    content: str
    round_number: int


@dataclass
class CouncilOutput:
    """Output completo del consejo."""

    brief: Brief
    group: str = "creativo_leyendas"
    proposals: list[AgentResponse] = field(default_factory=list)
    debate: list[AgentResponse] = field(default_factory=list)
    synthesis: str = ""
