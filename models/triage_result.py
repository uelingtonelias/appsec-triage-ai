from dataclasses import dataclass
from dataclasses import field


@dataclass
class TriageResult:

    # ==========================================
    # AI Classification
    # ==========================================

    classification: str

    confidence: int

    risk: str

    # ==========================================
    # AI Analysis
    # ==========================================

    reasoning: str

    developer_recommendation: str

    # ==========================================
    # Evidence
    # ==========================================

    evidence: list[str] = field(
        default_factory=list
    )

    # ==========================================
    # Optional Code Suggestion
    # ==========================================

    recommended_code: str = ""

    def is_true_positive(
        self
    ) -> bool:

        return (
            self.classification
            in [
                "True Positive",
                "Likely True Positive"
            ]
        )

    def is_false_positive(
        self
    ) -> bool:

        return (
            self.classification
            == "Likely False Positive"
        )

    def requires_review(
        self
    ) -> bool:

        return (
            self.classification
            == "Needs Review"
        )

    def to_dict(
        self
    ) -> dict:

        return {
            "classification":
                self.classification,

            "confidence":
                self.confidence,

            "risk":
                self.risk,

            "reasoning":
                self.reasoning,

            "developer_recommendation":
                self.developer_recommendation,

            "evidence":
                self.evidence,

            "recommended_code":
                self.recommended_code
        }