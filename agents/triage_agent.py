import json
from pathlib import Path
from llm.ollama_client import OllamaClient
from llm.prompt_builder import PromptBuilder
from models.repository_context import RepositoryContext
from tools.file_reader import FileReader
from tools.technology_detector import TechnologyDetector
from tools.context_builder import ContextBuilder


class TriageAgent:

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.llm = OllamaClient()
        self.prompt_builder = PromptBuilder()
        self.file_reader = FileReader()
        self.tech_detector = TechnologyDetector()

    def _build_context(
        self,
        finding
    ) -> RepositoryContext:
        tech = self.tech_detector.detect(
            self.repo_path
        )
        file_content = ""
        try:
            full_path = Path(
                finding.file_path
            )
            if not full_path.exists():
                full_path = (
                    Path(self.repo_path)
                    / finding.file_path
                )
            file_content = self.file_reader.read(
                str(full_path)
            )
        except Exception as ex:
            print(
                f"[WARN] Failed to read file "
                f"{finding.file_path}: {ex}"
            )
        return RepositoryContext(
            language=tech.get(
                "language",
                "Unknown"
            ),
            framework=tech.get(
                "framework",
                "Unknown"
            ),
            file_content=file_content[:1000],
            related_files=[]
        )
    def analyze(
        self,
        finding
    ):
        context = self._build_context(
            finding
        )
        print(
            f"[INFO] Rule: {finding.scanner_rule_id}"
        )
        print(
            f"[INFO] File: {finding.file_path}"
        )
        print(
            f"[INFO] Severity: {finding.severity}"
        )
        print(
            f"[INFO] Language: {context.language}"
        )
        print(
            f"[INFO] Framework: {context.framework}"
        )
        prompt = self.prompt_builder.build(
            finding,
            context
        )
        print(
            f"[INFO] Repository context size: "
            f"{len(context.file_content)}"
        )
        print(
            f"[INFO] Prompt size: "
            f"{len(prompt)} characters"
        )
        with open(
            "last-prompt.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(prompt)

        try:
            response = self.llm.ask(
                prompt
            )
            result = response["result"]
            metrics = response["metrics"]
            with open(
                "last-response.txt",
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    result,
                    file,
                    indent=2,
                    ensure_ascii=False
                )
            print(
                "[INFO] JSON validated successfully."
            )
            print(
                f"[INFO] Classification: "
                f"{result.get('classification')}"
            )
            print(
                f"[INFO] Confidence: "
                f"{result.get('confidence')}"
            )
            return {
                "result": result,
                "metrics": metrics
            }
        except Exception as ex:
            print(
                f"[ERROR] Analysis failed: {ex}"
            )
            return {
                "result": {
                    "classification": "Needs Review",
                    "confidence": 0,
                    "risk": getattr(
                        finding,
                        "severity",
                        "LOW"
                    ),
                    "reasoning": (
                        f"LLM processing failed: {str(ex)}"
                    ),
                    "evidence": [],
                    "developer_recommendation": (
                        "Manual review required."
                    ),
                    "recommended_code": ""
                },
                "metrics": {
                    "prompt_tokens": 0,
                    "response_tokens": 0,
                    "total_tokens": 0,
                    "elapsed_seconds": 0
                }
            }