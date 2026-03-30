---
name: scenario-simulation
description: Provides "What-If" testing for the production against specific constraints.
---
# Skill: Scenario Simulation

## Description
Provides "What-If" testing for the production (e.g., "What if the budget is cut by 20%?").

## Inputs
- `ProductionContext`: Aggregated data from all other skills.
- `ScenarioPreset`: The specific constraint to test.

## Outputs
- `ScenarioResult`: Strategic tradeoffs, impact summaries, and executive recommendations.

## Logic
- Leverages Gemini 3's high-level reasoning to simulate studio-level decision making.
- Provides a "Producer Sandbox" for stress-testing the script against realism.
