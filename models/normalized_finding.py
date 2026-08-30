from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional


@dataclass
class NormalizedFinding:

    # ==========================================
    # Scanner Metadata
    # ==========================================

    tool: str

    external_id: str

    scanner_rule_id: str

    # ==========================================
    # Core Finding Information
    # ==========================================

    title: str

    description: str

    severity: str

    cwe: Optional[int] = None

    # ==========================================
    # Location
    # ==========================================

    file_path: Optional[str] = None

    start_line: Optional[int] = None

    end_line: Optional[int] = None

    # ==========================================
    # Source Code
    # ==========================================

    code_snippet: Optional[str] = None

    # ==========================================
    # References
    # ==========================================

    references: list[str] = field(
        default_factory=list
    )

    # ==========================================
    # Dataflow (SAST)
    # ==========================================

    source: Optional[str] = None

    sink: Optional[str] = None

    dataflow: list[str] = field(
        default_factory=list
    )

    # ==========================================
    # Technology Metadata
    # ==========================================

    language: Optional[str] = None

    framework: Optional[str] = None

    package: Optional[str] = None

    # ==========================================
    # Repository Metadata
    # ==========================================

    repository: Optional[str] = None

    branch: Optional[str] = None

    commit: Optional[str] = None

    # ==========================================
    # Correlation
    # ==========================================

    fingerprint: Optional[str] = None

    # ==========================================
    # Original Scanner Payload
    # ==========================================

    raw_data: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def correlation_key(
        self
    ) -> str:

        return (
            f"{self.scanner_rule_id}|"
            f"{self.file_path}|"
            f"{self.start_line}"
        )

    def to_dict(
        self
    ) -> dict:

        return {
            "tool": self.tool,
            "external_id": self.external_id,
            "scanner_rule_id": self.scanner_rule_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "cwe": self.cwe,
            "file_path": self.file_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "code_snippet": self.code_snippet,
            "references": self.references,
            "source": self.source,
            "sink": self.sink,
            "dataflow": self.dataflow,
            "language": self.language,
            "framework": self.framework,
            "package": self.package,
            "repository": self.repository,
            "branch": self.branch,
            "commit": self.commit,
            "fingerprint": self.fingerprint,
            "correlation_key": self.correlation_key
        }