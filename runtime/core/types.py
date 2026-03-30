from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Scene:
    scene_number: int
    heading: str
    int_ext: str
    location: str
    day_night: str
    summary: str
    raw_text: str
    cast: List[str] = field(default_factory=list)
    props: List[str] = field(default_factory=list)
    action_tags: List[str] = field(default_factory=list)
    risk_keywords: List[str] = field(default_factory=list)

@dataclass
class SceneRisk:
    scene_number: int
    overall_risk_score: float
    safety_risk: float
    logistics_risk: float
    schedule_risk: float
    budget_risk: float
    compliance_risk: float
    risk_flags: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)

@dataclass
class BudgetPressure:
    scene_number: int
    pressure_band: str  # Low, Moderate, High, Extreme
    complexity_score: float
    cost_drivers: List[str] = field(default_factory=list)
    multipliers_applied: Dict[str, float] = field(default_factory=list)
    optimization_ideas: List[str] = field(default_factory=list)

@dataclass
class ScheduleIssue:
    scene_number: Optional[int]
    issue_type: str
    severity: str  # Low, Medium, High, Critical
    description: str
    recommendation: str

@dataclass
class ScenarioResult:
    preset_name: str
    changes_applied: List[str] = field(default_factory=list)
    tradeoffs: List[str] = field(default_factory=list)
    impact_summary: str = ""
    recommendations: List[str] = field(default_factory=list)

@dataclass
class ProducerReport:
    title: str
    project_summary: str
    scene_count: int
    top_risks: List[SceneRisk] = field(default_factory=list)
    top_budget_hotspots: List[BudgetPressure] = field(default_factory=list)
    schedule_warnings: List[ScheduleIssue] = field(default_factory=list)
    scenario_results: List[ScenarioResult] = field(default_factory=list)
    final_recommendations: List[List[str]] = field(default_factory=list)
    markdown: str = ""
