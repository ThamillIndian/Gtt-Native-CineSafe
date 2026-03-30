import os
from .core.types import ProducerReport
from .adapters.parser_adapter import parse_script
from .adapters.risk_adapter import analyze_risks
from .adapters.budget_adapter import analyze_budget_pressure
from .adapters.schedule_adapter import analyze_schedule
from .adapters.scenario_adapter import simulate_scenarios
from .adapters.report_adapter import build_report
from .file_store import FileStore
from .utils.logger import logger

def run_pipeline(script_text: str, scenario_preset: str = "standard") -> ProducerReport:
    logger.clear() # Reset logs for new run
    # 1. Parse
    logger.log("pipeline", "Starting CineSafe analysis flow...")
    scenes = parse_script(script_text)
    
    # 2. Analyze Risks
    print("[CineSafe] Analyzing production risks...")
    risks = analyze_risks(scenes)
    
    # 3. Analyze Budget Pressure
    print("[CineSafe] Estimating budget pressure...")
    budget_pressures = analyze_budget_pressure(scenes)
    
    # 4. Analyze Schedule
    print("[CineSafe] Evaluating schedule feasibility...")
    schedule_issues = analyze_schedule(scenes)
    
    # 5. Simulate Scenarios
    print(f"[CineSafe] Simulating scenario: {scenario_preset}...")
    scenario_results = simulate_scenarios(
        scenes, risks, budget_pressures, schedule_issues, preset=scenario_preset
    )
    
    # 6. Build Report
    print("[CineSafe] Generating final producer report...")
    report = build_report(
        scenes, risks, budget_pressures, schedule_issues, scenario_results
    )
    
    # 7. Save Outputs
    output_dir = os.path.join("outputs", "intermediate")
    os.makedirs(output_dir, exist_ok=True)
    
    FileStore.save_json(os.path.join(output_dir, "scenes.json"), [vars(s) for s in scenes])
    FileStore.save_json(os.path.join(output_dir, "risks.json"), [vars(r) for r in risks])
    FileStore.save_json(os.path.join(output_dir, "budget.json"), [vars(b) for b in budget_pressures])
    FileStore.save_json(os.path.join(output_dir, "schedule.json"), [vars(i) for i in schedule_issues])
    
    report_path = os.path.join("outputs", "reports", "latest_report.md")
    FileStore.save_markdown(report_path, report.markdown)
    
    return report

if __name__ == "__main__":
    sample_path = os.path.join("examples", "sample_script.txt")
    if os.path.exists(sample_path):
        with open(sample_path, 'r', encoding='utf-8') as f:
            script = f.read()
        
        run_pipeline(script)
        print("\nPipeline execution complete.")
