"""Orquestador del Consejo de Dirección de AdmiraNext."""

from __future__ import annotations

import concurrent.futures
from typing import Callable, Optional

import anthropic

from admiranext.agents.base import CouncilAgent
from admiranext.agents.creativo.leyendas import CCO, CDO, CXO, CSO
from admiranext.agents.creativo.coetaneos import CCO_Coetaneo, CDO_Coetaneo, CXO_Coetaneo, CSO_Coetaneo
from admiranext.agents.racional.leyendas import CEO, CTO, COO, CFO
from admiranext.agents.racional.coetaneos import CEO_Coetaneo, CTO_Coetaneo, COO_Coetaneo, CFO_Coetaneo
from admiranext.models import AgentResponse, Brief, CouncilOutput


GROUPS = {
    "leyendas": {
        "label": "⭐ Consejo Leyendas",
        "generation": "leyendas",
        "agents": [CEO, CTO, COO, CFO, CCO, CDO, CXO, CSO],
        "racional": [CEO, CTO, COO, CFO],
        "creativo": [CCO, CDO, CXO, CSO],
    },
    "coetaneos": {
        "label": "🚀 Consejo Coetáneos",
        "generation": "coetaneos",
        "agents": [CEO_Coetaneo, CTO_Coetaneo, COO_Coetaneo, CFO_Coetaneo, CCO_Coetaneo, CDO_Coetaneo, CXO_Coetaneo, CSO_Coetaneo],
        "racional": [CEO_Coetaneo, CTO_Coetaneo, COO_Coetaneo, CFO_Coetaneo],
        "creativo": [CCO_Coetaneo, CDO_Coetaneo, CXO_Coetaneo, CSO_Coetaneo],
    },
}


class Council:
    """Orquesta el debate colaborativo entre los 4 agentes del consejo."""

    def __init__(self, group: str = "leyendas", client: Optional[anthropic.Anthropic] = None):
        self.client = client or anthropic.Anthropic()
        self.group = group

        group_config = GROUPS.get(group, GROUPS["leyendas"])
        self.group_label = group_config["label"]
        self.agents = [
            agent_cls(client=self.client) for agent_cls in group_config["agents"]
        ]
        self.leader = self.agents[0]  # CEO lidera la síntesis

    def run(
        self,
        brief: Brief,
        on_proposal: Optional[Callable] = None,
        on_debate: Optional[Callable] = None,
        on_synthesis: Optional[Callable] = None,
    ) -> CouncilOutput:
        """Ejecuta el flujo completo del consejo."""
        output = CouncilOutput(brief=brief, group=self.group)
        brief_text = brief.to_prompt()

        # Ronda 1: Propuestas individuales (en paralelo)
        proposals = self._run_parallel(
            [(agent.propose, brief_text) for agent in self.agents],
            callback=on_proposal,
        )
        output.proposals = proposals

        # Ronda 2: Debate (en paralelo)
        debate_responses = self._run_parallel(
            [(agent.debate, brief_text, proposals) for agent in self.agents],
            callback=on_debate,
        )
        output.debate = debate_responses

        # Síntesis final por el líder
        all_contributions = proposals + debate_responses
        synthesis = self.leader.synthesize(brief_text, all_contributions)
        output.synthesis = synthesis
        if on_synthesis:
            on_synthesis(synthesis)

        return output

    def _run_parallel(
        self,
        tasks: list,
        callback: Optional[Callable] = None,
    ) -> list:
        """Ejecuta tareas de agentes en paralelo usando threads."""
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for task in tasks:
                fn = task[0]
                args = task[1:]
                future = executor.submit(fn, *args)
                futures[future] = fn

            for future in concurrent.futures.as_completed(futures):
                response = future.result()
                results.append(response)
                if callback:
                    callback(response)

        return results
