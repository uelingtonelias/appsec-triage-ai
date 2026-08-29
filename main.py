import argparse
from parsers.semgrep_parser import SemgrepParser
from agents.triage_agent import TriageAgent

parser = argparse.ArgumentParser()
parser.add_argument(
    "--report",
    required=True
)
parser.add_argument(
    "--repo",
    required=True
)
args = parser.parse_args()
findings = SemgrepParser().parse(
    args.report
)
findings = findings[:1]
agent = TriageAgent(
    repo_path=args.repo
    )
for finding in findings:
    result = agent.analyze(
        finding
    )
    print(result)