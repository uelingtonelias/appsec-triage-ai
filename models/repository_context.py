from dataclasses import dataclass

@dataclass
class RepositoryContext:
    file_content: str
    related_files: list
    framework: str = ""
    language: str = ""