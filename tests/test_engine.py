import pytest
from runtime.adapters.parser_adapter import parse_script
from runtime.adapters.risk_adapter import analyze_risks

def test_parser_splits_scenes():
    script = "INT. OFFICE - DAY\nLine 1\nEXT. STREET - NIGHT\nLine 2"
    scenes = parse_script(script)
    assert len(scenes) == 2
    assert scenes[0].location == "OFFICE"
    assert scenes[1].day_night == "NIGHT"

def test_risk_adapter_detects_flags():
    from runtime.core.types import Scene
    scene = Scene(
        scene_number=1,
        heading="EXT. STREET - NIGHT",
        int_ext="EXT.",
        location="STREET",
        day_night="NIGHT",
        summary="A chase with a gun.",
        raw_text="A chase with a gun.",
        action_tags=["CHASE"],
        risk_keywords=["GUN"]
    )
    from runtime.adapters.risk_adapter import RiskAdapter
    adapter = RiskAdapter()
    risk = adapter.calculate_scene_risk(scene)
    assert "GUN" in risk.risk_flags
    assert risk.overall_risk_score > 0
