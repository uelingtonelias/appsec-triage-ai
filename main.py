import argparse

from parsers.semgrep_parser import SemgrepParser
from agents.triage_agent import TriageAgent
from tools.triage_ignore import TriageIgnore
from output.defectdojo_api import DefectDojoApi


SEPARATOR = "=" * 60


CLASSIFICATIONS = {
    "True Positive": 0,
    "Likely True Positive": 0,
    "Needs Review": 0,
    "Likely False Positive": 0
}


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--report",
        required=True
    )

    parser.add_argument(
        "--repo",
        required=True
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help=(
            "Number of findings to process. "
            "Use 0 for all findings."
        )
    )

    parser.add_argument(
        "--dojo-url"
    )

    parser.add_argument(
        "--dojo-token"
    )

    parser.add_argument(
        "--dojo-product"
    )

    args = parser.parse_args()

    parser_instance = SemgrepParser()

    findings = parser_instance.parse(
        args.report
    )

    print(
        f"[INFO] Findings loaded: "
        f"{len(findings)}"
    )

    ignore = TriageIgnore()

    filtered_findings = []

    ignored_count = 0

    ignored_rules = {}

    for finding in findings:

        if ignore.should_ignore(
            finding
        ):

            ignored_count += 1

            ignored_rules[
                finding.scanner_rule_id
            ] = (
                ignored_rules.get(
                    finding.scanner_rule_id,
                    0
                ) + 1
            )

            print(
                f"[INFO] Ignored: "
                f"{finding.scanner_rule_id} | "
                f"{finding.file_path}"
            )

            continue

        filtered_findings.append(
            finding
        )

    findings = filtered_findings

    print(
        f"[INFO] Ignored findings: "
        f"{ignored_count}"
    )

    if args.limit > 0:

        findings = findings[:args.limit]

    print(
        f"[INFO] Findings selected: "
        f"{len(findings)}"
    )

    agent = TriageAgent(
        args.repo
    )

    dojo = None

    dojo_test_id = None

    if (
        args.dojo_url
        and args.dojo_token
        and args.dojo_product
    ):

        dojo = DefectDojoApi(
            url=args.dojo_url,
            token=args.dojo_token
        )

        dojo_info = (
            dojo.get_product_and_semgrep_test(
                product_name=args.dojo_product
            )
        )

        dojo_test_id = dojo_info[
            "test_id"
        ]

        print(
            f"[INFO] Product ID: "
            f"{dojo_info['product_id']}"
        )

        print(
            f"[INFO] Engagement ID: "
            f"{dojo_info['engagement_id']}"
        )

        print(
            f"[INFO] Semgrep Test ID: "
            f"{dojo_info['test_id']}"
        )

    total_prompt_tokens = 0
    total_response_tokens = 0
    total_tokens = 0
    total_seconds = 0

    processed = 0

    classifications = dict(
        CLASSIFICATIONS
    )

    dojo_uploaded = 0

    for index, finding in enumerate(
        findings,
        start=1
    ):

        print("\n")
        print(SEPARATOR)

        print(
            f"[INFO] Processing finding "
            f"{index}/{len(findings)}"
        )

        print(SEPARATOR)

        response = agent.analyze(
            finding
        )

        if not response:
            continue

        result = response.get(
            "result",
            {}
        )

        metrics = response.get(
            "metrics",
            {}
        )

        processed += 1

        total_prompt_tokens += (
            metrics.get(
                "prompt_tokens",
                0
            )
        )

        total_response_tokens += (
            metrics.get(
                "response_tokens",
                0
            )
        )

        total_tokens += (
            metrics.get(
                "total_tokens",
                0
            )
        )

        total_seconds += (
            metrics.get(
                "elapsed_seconds",
                0
            )
        )

        classification = result.get(
            "classification",
            "Needs Review"
        )

        if classification in classifications:

            classifications[
                classification
            ] += 1

        print("\n[RESULT]")

        print(result)

                #
        # Update Finding in DefectDojo
        #
        if dojo and dojo_test_id:

            try:

                updated = (
                    dojo.append_ai_triage_review(
                        test_id=dojo_test_id,
                        rule_id=(
                            finding.scanner_rule_id
                        ),
                        file_path=(
                            finding.file_path
                        ),
                        line=getattr(
                            finding,
                            "start_line",
                            0
                        ),
                        result=result
                    )
                )

                if updated:

                    dojo_uploaded += 1

                    print(
                        "[INFO] Finding updated "
                        "in DefectDojo."
                    )

                else:

                    print(
                        "[INFO] Finding not found "
                        "in DefectDojo."
                    )

            except Exception as ex:

                print(
                    f"[WARN] Failed to update "
                    f"finding: {ex}"
                )

    print("\n")
    print(SEPARATOR)
    print("TRIAGE SUMMARY")
    print(SEPARATOR)

    print(
        f"Model              : "
        f"{agent.llm.model}"
    )

    print(
        f"Findings Loaded    : "
        f"{len(filtered_findings) + ignored_count}"
    )

    print(
        f"Findings Ignored   : "
        f"{ignored_count}"
    )

    print(
        f"Findings Processed : "
        f"{processed}"
    )

    print("\nCLASSIFICATIONS")

    for key, value in classifications.items():

        print(
            f"  {key:<22}: {value}"
        )

    print("\nTOKEN USAGE")

    print(
        f"  Prompt Tokens    : "
        f"{total_prompt_tokens}"
    )

    print(
        f"  Response Tokens  : "
        f"{total_response_tokens}"
    )

    print(
        f"  Total Tokens     : "
        f"{total_tokens}"
    )

    if processed > 0:

        print(
            f"  Avg Prompt Tokens: "
            f"{total_prompt_tokens / processed:.2f}"
        )

        print(
            f"  Avg Resp Tokens  : "
            f"{total_response_tokens / processed:.2f}"
        )

    print("\nPERFORMANCE")

    print(
        f"  Total Time (s)   : "
        f"{total_seconds:.2f}"
    )

    print(
        f"  Total Time (min) : "
        f"{total_seconds / 60:.2f}"
    )

    if processed > 0:

        print(
            f"  Avg Time/Finding : "
            f"{total_seconds / processed:.2f}s"
        )

        print(
            f"  Avg Tokens       : "
            f"{total_tokens / processed:.2f}"
        )

    if total_seconds > 0:

        print(
            f"  Tokens/Second    : "
            f"{total_tokens / total_seconds:.2f}"
        )

        print(
            f"  Avg Time/Token   : "
            f"{total_seconds / total_tokens:.4f}s"
        )

    if ignored_rules:

        print("\nIGNORED RULES")

        for rule, count in sorted(
            ignored_rules.items(),
            key=lambda item: item[1],
            reverse=True
        ):

            print(
                f"  {count:<5} {rule}"
            )

    if dojo:

        print("\nDEFECTDOJO")

        print(
            f"  Product         : "
            f"{args.dojo_product}"
        )

        print(
            f"  Findings Updated: "
            f"{dojo_uploaded}"
        )

    print("\nDONE")


if __name__ == "__main__":
    main()