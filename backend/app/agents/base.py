"""
Base Agent — abstract interface for all swarm agents.
"""

import time
import traceback
from abc import ABC, abstractmethod
from typing import Any

from anthropic import Anthropic

from app.config import settings
from app.models import AgentOutput


class BaseAgent(ABC):
    """Abstract base class for all swarm agents."""

    name: str = "base_agent"
    description: str = "Base agent"

    def __init__(self):
        self.client = None
        if settings.anthropic_api_key:
            self.client = Anthropic(api_key=settings.anthropic_api_key)

    def _llm_call(self, system_prompt: str, user_prompt: str) -> str:
        """Make a call to Claude 3.5 with the given prompts."""
        if not self.client:
            return f"[MOCK LLM] {self.name}: Analysis complete based on available data."

        try:
            response = self.client.messages.create(
                model=settings.anthropic_model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1500,
            )
            return response.content[0].text
        except Exception as e:
            return f"[LLM Error] {self.name}: {str(e)}"

    @abstractmethod
    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the agent's analysis.

        Args:
            state: The current SwarmState dictionary.

        Returns:
            Dict with keys to merge back into SwarmState.
        """
        ...

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Wrapper that handles timing, error catching, and status updates.
        """
        start = time.time()
        try:
            result = self.execute(state)
            elapsed = (time.time() - start) * 1000

            # Get the agent's specific output for status tracking
            agent_outputs = result.get("agent_outputs", {})
            my_output = agent_outputs.get(self.name, {})
            
            status_update = {
                "agent_name": self.name,
                "status": "complete",
                "summary": my_output.get("summary", ""),
                "confidence": my_output.get("confidence", 0.5),
                "execution_time_ms": elapsed,
            }

            # Return the full result plus our status updates
            final_result = {**result}
            final_result["agent_statuses"] = [status_update]
            final_result["errors"] = []
            return final_result

        except Exception as e:
            elapsed = (time.time() - start) * 1000
            error_msg = f"{self.name} failed: {str(e)}\n{traceback.format_exc()}"

            return {
                "agent_outputs": {
                    self.name: {
                        "agent_name": self.name,
                        "confidence": 0.0,
                        "signal": "neutral",
                        "score": 50.0,
                        "summary": f"Agent failed: {str(e)}",
                        "data": {},
                        "key_findings": [f"Error: {str(e)}"],
                    }
                },
                "agent_statuses": [{
                    "agent_name": self.name,
                    "status": "error",
                    "summary": str(e),
                    "confidence": 0.0,
                    "execution_time_ms": elapsed,
                }],
                "errors": [error_msg],
            }

    def _make_output(
        self,
        confidence: float,
        signal: str,
        score: float,
        summary: str,
        data: dict = None,
        key_findings: list[str] = None,
    ) -> dict[str, Any]:
        """Helper to construct a standardized agent output dict."""
        return {
            "agent_outputs": {
                self.name: {
                    "agent_name": self.name,
                    "confidence": confidence,
                    "signal": signal,
                    "score": score,
                    "summary": summary,
                    "data": data or {},
                    "key_findings": key_findings or [],
                }
            }
        }
