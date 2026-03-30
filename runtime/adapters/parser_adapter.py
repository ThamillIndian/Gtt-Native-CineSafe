import re
from typing import List
from ..core.types import Scene
from ..utils.logger import logger

class ScreenplayParser:
    # Scene heading patterns: supports INT., EXT., VARIOUS, and decimal numbering (e.g., 4.1.INT.)
    SCENE_HEADING_PATTERN = re.compile(
        r'^\s*(?:\d+(?:\.\d+)*\.?\s*)?(INT\.|EXT\.|INT/EXT\.|I/E\.|INT\./EXT\.|VARIOUS)\s+(.+?)(?:\s+-\s+(.+))?$', 
        re.IGNORECASE | re.MULTILINE
    )

    # Common risk/action keywords
    ACTION_TAGS = ["CHASE", "FIGHT", "STUNT", "CROWD", "TRAFFIC", "EXPLOSION", "FIRE", "WATER"]
    RISK_KEYWORDS = ["GUN", "KNIFE", "WEAPON", "BLOOD", "DEATH", "MINOR", "ANIMAL", "NIGHT", "STORM"]

    @staticmethod
    def parse_script(script_text: str) -> List[Scene]:
        scenes = []
        lines = script_text.splitlines()
        
        current_scene_data = None
        scene_count = 0
        logger.log("parser", f"Starting parse of {len(script_text)} characters...")
        
        # Split text into scene blocks first
        scene_blocks = []
        last_match_start = 0
        matches = list(ScreenplayParser.SCENE_HEADING_PATTERN.finditer(script_text))
        
        for i, match in enumerate(matches):
            if i > 0:
                scene_blocks.append((matches[i-1], script_text[last_match_start:match.start()]))
            last_match_start = match.start()
        
        if matches:
            scene_blocks.append((matches[-1], script_text[last_match_start:]))

        for match, block_text in scene_blocks:
            scene_count += 1
            int_ext = match.group(1).upper()
            location = match.group(2).strip().upper()
            day_night = (match.group(3) or "DAY").strip().upper()
            
            # Simple metadata extraction
            action_tags = [tag for tag in ScreenplayParser.ACTION_TAGS if tag in block_text.upper()]
            risk_keywords = [word for word in ScreenplayParser.RISK_KEYWORDS if word in block_text.upper()]
            
            # Use LLM for a quick summary if needed, but for v1, just take first few lines
            summary_lines = [l.strip() for l in block_text.splitlines() if l.strip() and not ScreenplayParser.SCENE_HEADING_PATTERN.match(l)]
            summary = " ".join(summary_lines[:2]) + "..." if summary_lines else "No description."

            scene = Scene(
                scene_number=scene_count,
                heading=match.group(0),
                int_ext=int_ext,
                location=location,
                day_night=day_night,
                summary=summary,
                raw_text=block_text,
                action_tags=action_tags,
                risk_keywords=risk_keywords
            )
            scenes.append(scene)
            
        if not scenes and script_text.strip():
            # Fallback: Treat entire script as one scene if no headings found
            scenes.append(Scene(
                scene_number=1,
                heading="[FULL SCRIPT FALLBACK]",
                int_ext="N/A",
                location="UNKNOWN",
                day_night="N/A",
                summary="System could not detect scene headings. Analyzing full text as a single block.",
                raw_text=script_text,
                action_tags=[tag for tag in ScreenplayParser.ACTION_TAGS if tag in script_text.upper()],
                risk_keywords=[word for word in ScreenplayParser.RISK_KEYWORDS if word in script_text.upper()]
            ))
            
        logger.log("parser", f"Successfully parsed {len(scenes)} scenes.")
        return scenes

# Convenience function
def parse_script(script_text: str) -> List[Scene]:
    return ScreenplayParser.parse_script(script_text)
