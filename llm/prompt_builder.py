from pathlib import Path


class PromptBuilder:

    def __init__(self):

        self.system_prompt = Path(
            "prompts/system_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

        self.triage_prompt = Path(
            "prompts/triage_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

    def build(
        self,
        finding,
        repository_context
    ):

        system_prompt = self.system_prompt

        system_prompt = system_prompt.replace(
            "{language}",
            repository_context.language
        )

        system_prompt = system_prompt.replace(
            "{framework}",
            repository_context.framework
        )

        triage_prompt = self.triage_prompt

        replacements = {
            "language": repository_context.language,
            "framework": repository_context.framework,
            "rule_id": finding.rule_id,
            "severity": finding.severity,
            "cwe": str(
                getattr(
                    finding,
                    "cwe",
                    "Unknown"
                )
            ),
            "message": finding.message,
            "file_path": finding.file_path,
            "start_line": str(
                getattr(
                    finding,
                    "start_line",
                    0
                )
            ),
            "end_line": str(
                getattr(
                    finding,
                    "end_line",
                    0
                )
            ),
            "code_snippet": str(
                getattr(
                    finding,
                    "code_snippet",
                    ""
                )
            ),
            "source": str(
                getattr(
                    finding,
                    "source",
                    ""
                )
            ),
            "dataflow": str(
                getattr(
                    finding,
                    "dataflow",
                    ""
                )
            ),
            "sink": str(
                getattr(
                    finding,
                    "sink",
                    ""
                )
            ),
            "repository_context": repository_context.file_content,
            "related_files": "\n".join(
                repository_context.related_files
            )
        }

        for key, value in replacements.items():

            triage_prompt = triage_prompt.replace(
                f"{{{key}}}",
                value
            )

        return f"""
SYSTEM INSTRUCTIONS
===================

{system_prompt}

FINDING ANALYSIS
================

{triage_prompt}
"""