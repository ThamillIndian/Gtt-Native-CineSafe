# Skill: Script Intake

## Description
This skill parses raw screenplay text files into structured Python objects (`Scene` dataclasses). It uses regex to identify scene headings, INT/EXT tags, and locations.

## Inputs
- `script_text`: The raw text of the screenplay.

## Outputs
- `List[Scene]`: A list of structured scene objects containing metadata and raw content.

## Logic
1. Identifies scene boundaries using standardized slugline patterns (e.g., `INT. OFFICE - DAY`).
2. Extracts location, time of day, and interior/exterior status.
3. Tags scenes with action keywords (STUNT, CHASE, etc.) using keyword matching.
