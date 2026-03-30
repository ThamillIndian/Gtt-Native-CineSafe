from typing import List, Optional
from ..core.types import Scene, ScheduleIssue

class ScheduleAdapter:
    def analyze_schedule(self, scenes: List[Scene]) -> List[ScheduleIssue]:
        issues = []
        
        # 1. Location Clustering (Repeated locations)
        location_counts = {}
        for scene in scenes:
            loc = scene.location.upper()
            if loc not in location_counts:
                location_counts[loc] = []
            location_counts[loc].append(scene.scene_number)
            
        for loc, scene_nums in location_counts.items():
            if len(scene_nums) > 1:
                # This isn't an "issue" but a clustering opportunity, we'll mark as Low severity/Recommendation
                issues.append(ScheduleIssue(
                    scene_number=None,
                    issue_type="Clustering Opportunity",
                    severity="Low",
                    description=f"Location '{loc}' appears in {len(scene_nums)} scenes.",
                    recommendation=f"Cluster scenes {', '.join(map(str, scene_nums))} to avoid unnecessary company moves."
                ))

        # 2. Sequential Company Moves
        for i in range(len(scenes) - 1):
            if scenes[i].location != scenes[i+1].location:
                # Potential move pressure
                pass # Logic could be added here for travel time heuristics

        # 3. Night Shoot Fragmentation
        night_scenes = [s for s in scenes if s.day_night == "NIGHT"]
        if len(night_scenes) > 0 and len(night_scenes) < len(scenes) * 0.2:
            issues.append(ScheduleIssue(
                scene_number=None,
                issue_type="Turnaround Pressure",
                severity="Medium",
                description="Small number of night scenes scattered across the script.",
                recommendation="Review turnaround times for crew. Consider shooting all night scenes in a single block if possible."
            ))

        # 4. High Complexity Concentration
        # (This would ideally use data from BudgetPressure, but for v1 we check tags)
        heavy_scenes = [s for s in scenes if any(t in ["STUNT", "FIRE", "EXPLOSION", "WATER"] for t in s.action_tags)]
        if len(heavy_scenes) > 2:
                issues.append(ScheduleIssue(
                scene_number=None,
                issue_type="Production Intensity",
                severity="High",
                description=f"Found {len(heavy_scenes)} high-intensity scenes.",
                recommendation="Ensure these scenes are not scheduled on consecutive days to prevent crew burnout."
            ))

        return issues

# Convenience function
def analyze_schedule(scenes: List[Scene]) -> List[ScheduleIssue]:
    adapter = ScheduleAdapter()
    return adapter.analyze_schedule(scenes)
