# Skill: Scene Risk Analysis

## Description
Analyzes individual scenes for production risks, safety hazards, and compliance requirements.

## Inputs
- `List[Scene]`: Structured scenes from the intake skill.

## Outputs
- `List[SceneRisk]`: Detailed risk scores and mitigation strategies.

## Logic
- **Deterministic**: Checks for keywords like "FIRE", "WATER", "GUN", "CHILD" and cross-references with `risk_weights.csv`.
- **Qualitative**: Uses Gemini 2.0 to provide nuanced mitigation advice and overall risk context.
- **Scoring**: Calculates an 1-10 risk score based on grounded weights.
