---
name: schedule-feasibility-check
description: Evaluates the logistical feasibility of the production schedule.
---
# Skill: Schedule Feasibility Check

## Description
Evaluates the logistical feasibility of the production schedule based on location clustering and turnaround times.

## Inputs
- `List[Scene]`: Parsed screenplay scenes.

## Outputs
- `List[ScheduleIssue]`: Warnings about location moves, night shoots, and burnout risks.

## Logic
- Counts location occurrences to suggest clustering opportunities.
- Identifies "Company Move" pressure when locations change frequently.
- Flags turnaround issues for night-to-day transitions.
