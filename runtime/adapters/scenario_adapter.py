from typing import List
from ..core.types import Scene, SceneRisk, BudgetPressure, ScheduleIssue, ScenarioResult
from ..llm_client import default_client

class ScenarioAdapter:
    PRESETS = {
        "standard": "Follow the baseline production plan.",
        "budget_cut_20": "Reduce total production budget by 20%.",
        "accelerate_timeline": "Shorten the shooting schedule by 15%.",
        "max_safety": "Prioritize safety and compliance above all else."
    }

    def simulate_scenarios(
        self,
        scenes: List[Scene],
        risks: List[SceneRisk],
        budget_pressures: List[BudgetPressure],
        schedule_issues: List[ScheduleIssue],
        preset: str = "standard"
    ) -> List[ScenarioResult]:
        
        prompt = f"""
        Simulate a production scenario for this film project.
        Scenario Preset: {preset} ({self.PRESETS.get(preset, "")})
        
        Project Stats:
        - Total Scenes: {len(scenes)}
        - High-risk Scenes: {len([r for r in risks if r.overall_risk_score > 7])}
        - High-pressure Scenes: {len([b for b in budget_pressures if b.pressure_band in ["High", "Extreme"]])}
        
        Explain the tradeoffs and impact of this scenario on the project.
        Format as JSON with keys: "changes_applied" (list), "tradeoffs" (list), "impact_summary" (string), "recommendations" (list).
        """
        
        analysis = default_client.generate_json(prompt, "You are a realistic Movie Studio Head.")
        
        return [ScenarioResult(
            preset_name=preset,
            changes_applied=analysis.get("changes_applied", []),
            tradeoffs=analysis.get("tradeoffs", []),
            impact_summary=analysis.get("impact_summary", "Strategic adjustment to current production constraints."),
            recommendations=analysis.get("recommendations", [])
        )]

# Convenience function
def simulate_scenarios(scenes, risks, budget_pressures, schedule_issues, preset="standard"):
    adapter = ScenarioAdapter()
    return adapter.simulate_scenarios(scenes, risks, budget_pressures, schedule_issues, preset)
