from dataclasses import dataclass
from typing import List


@dataclass
class TriageResult:
    rule_id: str
    classification: str
    confidence: int
    risk: str
    reasoning: str
    remediation: str
    evidence: List[str]
    vulnerable_code: str
    recommended_code: str