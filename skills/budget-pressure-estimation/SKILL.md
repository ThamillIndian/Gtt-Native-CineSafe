---
name: budget-pressure-estimation
description: Estimates the financial strain of each scene based on production complexity.
---
# Skill: Budget Pressure Estimation

## Description
Estimates the financial strain of each scene based on production complexity.

## Inputs
- `List[Scene]`: Parsed screenplay scenes.

## Outputs
- `List[BudgetPressure]`: Pressure bands (Low, Moderate, High, Extreme) and optimization ideas.

## Logic
- Applies multipliers for high-cost factors (Night Exteriors, Crowds, Remote Locations).
- Returns practical "Producer Tips" for cost-saving measures via LLM generation.
