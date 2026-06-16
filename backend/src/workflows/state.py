from typing import List, Dict, Any
from pydantic import Field
from langgraph.graph import StateGraph

class ResearchState(StateGraph):
    query: str = Field(
        default="",
        description="User research query"
    )

    plan: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generated research plan"
    )

    target_audience: List[str] = Field(
        default_factory=list,
        description="Intended audience for the report"
    )

    selected_agents: List[str] = Field(
        default_factory=list,
        description="Agents selected to perform research tasks"
    )

    evidence: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Collected evidence from agents and sources"
    )

    synthesized_report: Dict[str, Any] = Field(
        default_factory=dict,
        description="Combined and synthesized findings"
    )

    verification_results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Fact-checking and verification output"
    )

    final_output: str = Field(
        default="",
        description="Final report delivered to the user"
    )

    errors: List[str] = Field(
        default_factory=list,
        description="Errors encountered during execution"
    )