import json
import os
import itertools
from typing import List, Dict, Any, Tuple

class AgriMindExpertSystem:
    def __init__(self, rules_filepath: str = "chemical_rules.json"):
        """
        Initializes the AgriMind Expert System by loading the rules knowledge base.
        """
        if not os.path.isabs(rules_filepath):
            # Resolve relative to the directory of this python file
            module_dir = os.path.dirname(os.path.abspath(__file__))
            self.rules_filepath = os.path.join(module_dir, rules_filepath)
        else:
            self.rules_filepath = rules_filepath
            
        self.chemicals = {}
        self.incompatibilities = {}
        self.load_rules()

    def load_rules(self):
        """
        Loads the chemical data and incompatibility rules from the JSON file.
        """
        if not os.path.exists(self.rules_filepath):
            # Fallback local rules if JSON file is missing
            self._load_fallback_rules()
            return

        try:
            with open(self.rules_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load chemicals
            for chem in data.get("chemicals", []):
                self.chemicals[chem["name"].lower()] = chem
            
            # Load incompatibilities (index by sorted tuple of chemical names for easy lookup)
            for rule in data.get("incompatibilities", []):
                chem1 = rule["chemical_1"].lower()
                chem2 = rule["chemical_2"].lower()
                key = tuple(sorted([chem1, chem2]))
                self.incompatibilities[key] = rule
        except Exception as e:
            print(f"Error loading rules JSON: {e}. Loading fallback rules.")
            self._load_fallback_rules()

    def _load_fallback_rules(self):
        """
        Fallback rules in case JSON is not available.
        """
        fallback_chems = [
            {"name": "Calcium Nitrate", "category": "Fertilizer", "active_ingredient": "Calcium, Nitrogen", "description": ""},
            {"name": "Magnesium Sulfate", "category": "Fertilizer", "active_ingredient": "Magnesium, Sulfur", "description": ""},
            {"name": "Bordeaux Mixture", "category": "Fungicide", "active_ingredient": "Copper Sulfate, Lime", "description": ""},
            {"name": "Chlorpyrifos", "category": "Insecticide", "active_ingredient": "Chlorpyrifos", "description": ""},
            {"name": "Lime Sulfur", "category": "Fungicide", "active_ingredient": "Calcium Polysulfide", "description": ""},
            {"name": "Neem Oil", "category": "Insecticide", "active_ingredient": "Azadirachtin", "description": ""}
        ]
        for chem in fallback_chems:
            self.chemicals[chem["name"].lower()] = chem

        fallback_rules = [
            {
                "chemical_1": "Calcium Nitrate",
                "chemical_2": "Magnesium Sulfate",
                "type": "Precipitation",
                "severity": "Blocked",
                "reason": "Forms insoluble Calcium Sulfate precipitate.",
                "alternative": "Apply separately."
            },
            {
                "chemical_1": "Bordeaux Mixture",
                "chemical_2": "Chlorpyrifos",
                "type": "Alkaline Hydrolysis",
                "severity": "Blocked",
                "reason": "Alkaline Bordeaux Mixture hydrolyzes Chlorpyrifos.",
                "alternative": "Apply separately."
            },
            {
                "chemical_1": "Lime Sulfur",
                "chemical_2": "Neem Oil",
                "type": "Phytotoxicity",
                "severity": "Blocked",
                "reason": "Sulfur combined with oils causes severe phytotoxicity.",
                "alternative": "Ensure 14-30 day interval between applications."
            }
        ]
        for rule in fallback_rules:
            chem1 = rule["chemical_1"].lower()
            chem2 = rule["chemical_2"].lower()
            key = tuple(sorted([chem1, chem2]))
            self.incompatibilities[key] = rule

    def get_chemical_info(self, name: str) -> Dict[str, Any]:
        """
        Returns info about a chemical by name, case-insensitive.
        """
        return self.chemicals.get(name.lower())

    def list_chemicals(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all chemicals registered in the system.
        """
        return list(self.chemicals.values())

    def validate_mixture(self, mixture_list: List[str]) -> Dict[str, Any]:
        """
        Validates a proposed mixture of chemicals.
        Checks all pair combinations for incompatibility rules.
        """
        report = {
            "proposed_mixture": mixture_list,
            "status": "Approved",
            "conflicts": [],
            "summary": "This mixture is safe to apply."
        }

        # Normalize chemical names and check existence
        normalized_mixture = []
        unknown_chemicals = []
        for chem in mixture_list:
            norm_chem = chem.strip()
            if norm_chem.lower() in self.chemicals:
                # Use standard casing from registry
                normalized_mixture.append(self.chemicals[norm_chem.lower()]["name"])
            else:
                unknown_chemicals.append(norm_chem)

        if unknown_chemicals:
            report["status"] = "Warning"
            report["summary"] = f"Warning: Contains unregistered chemicals: {', '.join(unknown_chemicals)}."
            report["conflicts"].append({
                "chemical_1": "Unknown",
                "chemical_2": ", ".join(unknown_chemicals),
                "type": "Unregistered Chemical Check",
                "severity": "Warning",
                "reason": f"Chemicals {unknown_chemicals} are not in the database. Mixing safety cannot be guaranteed.",
                "alternative": "Verify safety compatibility from handbook manually."
            })

        # Check pairs of registered chemicals
        if len(normalized_mixture) >= 2:
            pairs = list(itertools.combinations(normalized_mixture, 2))
            for chem1, chem2 in pairs:
                key = tuple(sorted([chem1.lower(), chem2.lower()]))
                if key in self.incompatibilities:
                    conflict = self.incompatibilities[key]
                    report["conflicts"].append({
                        "chemical_1": chem1,
                        "chemical_2": chem2,
                        "type": conflict["type"],
                        "severity": conflict["severity"],
                        "reason": conflict["reason"],
                        "alternative": conflict["alternative"]
                    })
                    # Upgrade severity
                    if conflict["severity"] == "Blocked":
                        report["status"] = "Blocked"
                    elif report["status"] != "Blocked" and conflict["severity"] == "Warning":
                        report["status"] = "Warning"

        # Update final summary
        blocked_count = sum(1 for c in report["conflicts"] if c["severity"] == "Blocked")
        warning_count = sum(1 for c in report["conflicts"] if c["severity"] == "Warning")
        
        if blocked_count > 0:
            report["status"] = "Blocked"
            report["summary"] = f"VETOED: Dangerous chemical combination detected! {blocked_count} blocked hazard(s) found."
        elif warning_count > 0:
            report["status"] = "Warning"
            report["summary"] = f"CAUTION: Potential hazards detected. {warning_count} warning(s) found."
            
        return report

    def add_rule(self, chemical_1: str, chemical_2: str, conflict_type: str, severity: str, reason: str, alternative: str):
        """
        Dynamically adds a rule to the active system.
        """
        rule = {
            "chemical_1": chemical_1,
            "chemical_2": chemical_2,
            "type": conflict_type,
            "severity": severity,
            "reason": reason,
            "alternative": alternative
        }
        key = tuple(sorted([chemical_1.lower(), chemical_2.lower()]))
        self.incompatibilities[key] = rule
