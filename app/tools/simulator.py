import json
import os
from typing import Dict, List, Any
from pydantic import BaseModel

class Scenario(BaseModel):
    id: str
    sector: str
    title: str
    description: str
    steps: List[Dict[str, Any]]
    
class TaskSimulator:
    def __init__(self):
        self.scenarios = self._load_scenarios()

    def _load_scenarios(self) -> Dict[str, Scenario]:
        scenarios = {}
        data_dir = os.path.join(os.getcwd(), "km_agent/data")
        
        # Load all scenario files
        scenario_files = [
            "solar_scenario.json",
            "agritech_scenario.json",
            "construction_scenario.json",
            "education_scenario.json",
            "water_scenario.json",
            "environment_scenario.json",
            "transport_scenario.json"
        ]
        
        for filename in scenario_files:
            scenario_path = os.path.join(data_dir, filename)
            if os.path.exists(scenario_path):
                with open(scenario_path, "r") as f:
                    data = json.load(f)
                    scenario = Scenario(**data)
                    scenarios[scenario.id] = scenario
        
        return scenarios

    def get_scenario(self, sector: str) -> Scenario:
        # Return the first scenario for the sector for now
        for scenario in self.scenarios.values():
            if scenario.sector == sector:
                return scenario
        return None

    def evaluate_step(self, scenario_id: str, step_index: int, user_action: str) -> Dict[str, Any]:
        """
        Evaluate the user's action against the scenario step.
        """
        scenario = self.scenarios.get(scenario_id)
        if not scenario:
            return {"error": "Scenario not found"}
        
        if step_index >= len(scenario.steps):
            return {"error": "Step index out of range"}
            
        step = scenario.steps[step_index]
        expected_action = step.get("expected_action")
        
        # Simple keyword matching for MVP
        # In real version, use LLM to evaluate semantic similarity
        is_correct = any(keyword in user_action.lower() for keyword in step.get("keywords", []))
        
        return {
            "correct": is_correct,
            "feedback": step.get("success_feedback") if is_correct else step.get("failure_feedback"),
            "next_step_index": step_index + 1 if is_correct else step_index
        }
