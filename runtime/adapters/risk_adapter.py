import csv
import os
from typing import List, Dict
from ..core.types import Scene, SceneRisk
from ..llm_client import default_client
from ..utils.logger import logger

class RiskAdapter:
    def __init__(self, weights_path: str = None):
        self.weights_path = weights_path or os.path.join(
            os.path.dirname(__file__), "..", "data", "risk_weights.csv"
        )
        self.weights = self.load_weights()

    def load_weights(self) -> Dict[str, Dict[str, float]]:
        weights = {}
        if not os.path.exists(self.weights_path):
            print(f"Warning: Risk weights file not found at {self.weights_path}")
            return weights
            
        with open(self.weights_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row['keyword'].upper()
                weights[keyword] = {
                    'safety': float(row['safety']),
                    'logistics': float(row['logistics']),
                    'schedule': float(row['schedule']),
                    'budget': float(row['budget']),
                    'compliance': float(row['compliance'])
                }
        return weights

    def analyze_risks(self, scenes: List[Scene]) -> List[SceneRisk]:
        results = []
        for scene in scenes:
            logger.log("risk", f"Analyzing Scene {scene.scene_number}: {scene.location}...")
            risk = self.calculate_scene_risk(scene)
            results.append(risk)
        return results

    def calculate_scene_risk(self, scene: Scene) -> SceneRisk:
        # 1. Deterministic Scoring
        scores = { 'safety': 0.0, 'logistics': 0.0, 'schedule': 0.0, 'budget': 0.0, 'compliance': 0.0 }
        risk_flags = []
        
        # Check explicit tags and keywords
        combined_cues = set(scene.action_tags + scene.risk_keywords)
        
        # Also check for EXTs and NIGHTs
        if scene.int_ext == "EXT.":
            combined_cues.add("EXTERIOR")
        if scene.day_night == "NIGHT":
            combined_cues.add("NIGHT")
            
        for cue in combined_cues:
            if cue in self.weights:
                risk_flags.append(cue)
                for pillar in scores:
                    scores[pillar] += self.weights[cue][pillar]
        
        # Max scores at 10.0 for v1
        for pillar in scores:
            scores[pillar] = min(10.0, scores[pillar])
            
        overall_score = sum(scores.values()) / 5.0
        
        # 2. LLM-powered explanation and mitigation (if risky)
        reasons = []
        mitigations = []
        
        if overall_score > 0:
            prompt = f"""
            Analyze the following screenplay scene for production risks. 
            Scene Heading: {scene.heading}
            Context: {scene.summary}
            Flags: {", ".join(risk_flags)}
            
            Based on these flags, identify the specific risks and suggest practical mitigations for a producer.
            Format the output as JSON with two keys: "reasons" (list of strings) and "mitigations" (list of strings).
            """
            
            analysis = default_client.generate_json(prompt, "You are a veteran Line Producer. Be practical and safety-conscious.")
            reasons = analysis.get("reasons", [f"Identified potential flags: {', '.join(risk_flags)}"])
            mitigations = analysis.get("mitigations", ["Consult with safety coordinators and experienced heads of department."])
        else:
            reasons = ["No major production risks identified in the text."]
            mitigations = ["Follow standard production safety protocols."]

        return SceneRisk(
            scene_number=scene.scene_number,
            overall_risk_score=round(overall_score, 1),
            safety_risk=round(scores['safety'], 1),
            logistics_risk=round(scores['logistics'], 1),
            schedule_risk=round(scores['schedule'], 1),
            budget_risk=round(scores['budget'], 1),
            compliance_risk=round(scores['compliance'], 1),
            risk_flags=risk_flags,
            reasons=reasons,
            mitigations=mitigations
        )

# Convenience function
def analyze_risks(scenes: List[Scene]) -> List[SceneRisk]:
    adapter = RiskAdapter()
    return adapter.analyze_risks(scenes)
