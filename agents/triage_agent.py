from pathlib import Path

from llm.ollama_client import OllamaClient
from llm.prompt_builder import PromptBuilder

from models.repository_context import RepositoryContext

from tools.file_reader import FileReader
from tools.technology_detector import TechnologyDetector
from tools.json_extractor import JsonExtractor


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
            language=tech["language"],
            framework=tech["framework"],
            file_content=file_content[:3000],
            related_files=[]
        )

    def analyze(self, finding):

        context = self._build_context(
            finding
        )

        print(
            f"[INFO] Rule: {finding.rule_id}"
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

        with open(
            "last-prompt.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(prompt)

        response = self.llm.ask(
            prompt
        )

        with open(
            "last-response.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(response)

        parsed = JsonExtractor.extract(
            response
        )

        if parsed:

            print(
                "[INFO] JSON extracted successfully."
            )

            return parsed

        print(
            "[WARN] Failed to extract JSON."
        )

        return {
            "classification": "Needs Review",
            "confidence": 0,
            "risk": "LOW",
            "reasoning": (
                "LLM returned invalid JSON."
            ),
            "evidence": [
                "Unable to parse model response."
            ],
            "developer_recommendation": (
                "Review model output manually."
            ),
            "recommended_code": "",
            "raw_response": response
        }