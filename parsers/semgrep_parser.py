import json

from models.finding import Finding


class SemgrepParser:

    def parse(self, report_path):

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            report = json.load(file)

        findings = []

        for result in report.get("results", []):

            source = ""
            sink = ""
            flow = ""

            try:

                trace = result.get(
                    "extra",
                    {}
                ).get(
                    "dataflow_trace",
                    {}
                )

                if trace:

                    if trace.get("taint_source"):

                        source = str(
                            trace["taint_source"]
                        )

                    if trace.get("taint_sink"):

                        sink = str(
                            trace["taint_sink"]
                        )

                    if trace.get(
                        "intermediate_vars"
                    ):

                        flow = " -> ".join(
                            [
                                str(x)
                                for x in trace[
                                    "intermediate_vars"
                                ]
                            ]
                        )

            except Exception:
                pass

            finding = Finding(

                rule_id=result.get(
                    "check_id",
                    ""
                ),

                severity=result.get(
                    "extra",
                    {}
                ).get(
                    "severity",
                    "UNKNOWN"
                ),

                file_path=result.get(
                    "path",
                    ""
                ),

                message=result.get(
                    "extra",
                    {}
                ).get(
                    "message",
                    ""
                ),

                start_line=result.get(
                    "start",
                    {}
                ).get(
                    "line",
                    0
                ),

                end_line=result.get(
                    "end",
                    {}
                ).get(
                    "line",
                    0
                ),

                code_snippet=result.get(
                    "extra",
                    {}
                ).get(
                    "lines",
                    ""
                ),

                source=source,

                sink=sink,

                dataflow=flow
            )

            findings.append(
                finding
            )

        return findings