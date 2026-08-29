from pathlib import Path

class FileReader:
    def read(self, file_path):
        return Path(file_path).read_text(
            encoding="utf8",
            errors="ignore"
        )
