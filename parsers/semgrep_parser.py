import json

from models.normalized_finding import (
    NormalizedFinding
)


class SemgrepParser:

    def parse(
        self,
        report_file
    ):

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        findings = []

        for result in data.get(
            "results",
            []
        ):

            findings.append(
                self._to_finding(
                    result
                )
            )

        return findings

    def _to_finding(
        self,
        result
    ):

        extra = result.get(
            "extra",
            {}
        )

        return NormalizedFinding(

            tool="Semgrep",

            external_id=result.get(
                "check_id",
                ""
            ),

            scanner_rule_id=result.get(
                "check_id",
                ""
            ),

            title=result.get(
                "check_id",
                ""
            ),

            description=extra.get(
                "message",
                ""
            ),

            severity=(
                extra.get(
                    "severity",
                    "INFO"
                ).upper()
            ),

            cwe=None,

            file_path=result.get(
                "path"
            ),

            start_line=result.get(
                "start",
                {}
            ).get(
                "line"
            ),

            end_line=result.get(
                "end",
                {}
            ).get(
                "line"
            ),

            code_snippet=extra.get(
                "lines",
                ""
            ),

            references=[],

            source=None,

            sink=None,

            dataflow=[],

            language=None,

            framework=None,

            package=None,

            repository=None,

            branch=None,

            commit=None,

            fingerprint=None,

            raw_data=result
        )