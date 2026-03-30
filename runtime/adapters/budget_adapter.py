import csv
import os
from typing import List, Dict
from ..core.types import Scene, BudgetPressure
from ..llm_client import default_client
from ..utils.logger import logger

class BudgetAdapter:
    def __init__(self, multipliers_path: str = None):
        self.multipliers_path = multipliers_path or os.path.join(
            os.path.dirname(__file__), "..", "data", "complexity_multipliers.csv"
        )
        self.multipliers = self.load_multipliers()

    def load_multipliers(self) -> Dict[str, float]:
        multipliers = {}
        if not os.path.exists(self.multipliers_path):
            return multipliers
        with open(self.multipliers_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                multipliers[row['factor'].upper()] = float(row['multiplier'])
        return multipliers

    def analyze_budget_pressure(self, scenes: List[Scene]) -> List[BudgetPressure]:
        logger.log("budget", f"Calculating budget pressure for {len(scenes)} scenes...")
        results = []
        for scene in scenes:
            pressure = self.calculate_scene_pressure(scene)
            results.append(pressure)
        return results

    def calculate_scene_pressure(self, scene: Scene) -> BudgetPressure:
        complexity_score = 1.0
        multipliers_applied = {}
        cost_drivers = []
        
        # 1. Apply deterministic multipliers
        if scene.day_night == "NIGHT" and scene.int_ext == "EXT.":
            m = self.multipliers.get("NIGHT_EXTERIOR", 1.5)
            complexity_score *= m
            multipliers_applied["NIGHT_EXTERIOR"] = m
            cost_drivers.append("Night Exterior Setup")
            
        if "CROWD" in scene.action_tags:
            m = self.multipliers.get("CROWD_50_PLUS", 1.4)
            complexity_score *= m
            multipliers_applied["CROWD"] = m
            cost_drivers.append("High Cast/Extra Count")
            
        # Detect other triggers
        for tag in scene.action_tags:
            if tag in ["FIRE", "EXPLOSION"]:
                m = self.multipliers.get("FIRE_EXPLOSION", 1.8)
                complexity_score *= m
                multipliers_applied[tag] = m
                cost_drivers.append(f"Pyrotechnics/SFX ({tag})")
            if tag == "STUNT":
                m = self.multipliers.get("STUNT_COMPLEX", 1.6)
                complexity_score *= m
                multipliers_applied["STUNT"] = m
                cost_drivers.append("Specialized Stunt Coordination")
        
        # 2. Classify pressure band
        if complexity_score > 3.0:
            pressure_band = "Extreme"
        elif complexity_score > 2.0:
            pressure_band = "High"
        elif complexity_score > 1.4:
            pressure_band = "Moderate"
        else:
            pressure_band = "Low"
            
        # 3. LLM-powered optimization ideas
        prompt = f"""
        Analyze the budget pressure for this film scene. 
        Scene: {scene.heading}
        Complexity Score: {complexity_score:.2f}
        Cost Drivers: {", ".join(cost_drivers)}
        
        Suggest 3 practical optimization ideas to reduce costs without destroying the creative vision.
        Format as JSON with key "optimization_ideas" (list of strings).
        """
        
        analysis = default_client.generate_json(prompt, "You are a cost-conscious Executive Producer.")
        optimization_ideas = analysis.get("optimization_ideas", ["Consider studio consolidation.", "Optimize crew travel schedules."])

        return BudgetPressure(
            scene_number=scene.scene_number,
            pressure_band=pressure_band,
            complexity_score=round(complexity_score, 2),
            cost_drivers=cost_drivers,
            multipliers_applied=multipliers_applied,
            optimization_ideas=optimization_ideas
        )

# Convenience function
def analyze_budget_pressure(scenes: List[Scene]) -> List[BudgetPressure]:
    adapter = BudgetAdapter()
    return adapter.analyze_budget_pressure(scenes)
