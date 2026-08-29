from dataclasses import dataclass

@dataclass
class Finding:

    rule_id: str
    severity: str
    file_path: str
    message: str

    start_line: int = 0
    end_line: int = 0

    code_snippet: str = ""

    source: str = ""
    sink: str = ""
    dataflow: str = ""

    cwe: str = "Unknown"