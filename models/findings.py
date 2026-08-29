from dataclasses import dataclass
from typing import Optional

@dataclass
class Finding:
    rule_id: str
    severity: str
    file_path: str
    message: str
    start_line: int = 0
    end_line: int = 0
    code_snippet: str = ""
    source: Optional[str] = None
    sink: Optional[str] = None
    dataflow: Optional[str] = None
