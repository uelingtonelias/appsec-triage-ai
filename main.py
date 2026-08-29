import argparse

from parsers.semgrep_parser import SemgrepParser
from agents.triage_agent import TriageAgent


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
        default=10,
        help="Number of findings to process. Use 0 for all findings."
    )

    args = parser.parse_args()

    parser_instance = SemgrepParser()

    findings = parser_instance.parse(
        args.report
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

    total_prompt_tokens = 0
    total_response_tokens = 0
    total_tokens = 0
    total_seconds = 0

    processed = 0

    classifications = dict(
        CLASSIFICATIONS
    )

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

        result = response["result"]

        metrics = response["metrics"]

        processed += 1

        total_prompt_tokens += (
            metrics["prompt_tokens"]
        )

        total_response_tokens += (
            metrics["response_tokens"]
        )

        total_tokens += (
            metrics["total_tokens"]
        )

        total_seconds += (
            metrics["elapsed_seconds"]
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

    print("\n")
    print(SEPARATOR)
    print("TRIAGE SUMMARY")
    print(SEPARATOR)

    print(
        f"Model              : "
        f"{agent.llm.model}"
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

    print("\nDONE")


if __name__ == "__main__":
    main()