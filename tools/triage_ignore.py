from pathlib import Path
from fnmatch import fnmatch

class TriageIgnore:
    def __init__(
        self,
        ignore_file=".triageignore"
    ):
        self.patterns = []
        path = Path(ignore_file)
        if not path.exists():
            return
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines():
            line = line.strip()
            if (
                not line
                or line.startswith("#")
            ):
                continue
            self.patterns.append(line)
    def should_ignore(
        self,
        finding
    ):
        file_path = (
            finding.file_path or ""
        ).replace("\\", "/")
        rule_id = (
            finding.scanner_rule_id or ""
        )
        for pattern in self.patterns:
            if pattern.startswith(
                "rule:"
            ):
                rule_pattern = pattern[5:]
                if fnmatch(
                    rule_id,
                    rule_pattern
                ):
                    return True
            else:
                if fnmatch(
                    file_path,
                    pattern
                ):
                    return True
        return False