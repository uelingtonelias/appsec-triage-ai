# AI-Triage

AI-Triage is an AI-powered Application Security Triage Agent designed to analyze SAST findings, reduce false positives, and provide actionable security guidance for developers.

The project analyzes Semgrep findings using repository context, framework awareness, and LLM-based reasoning to determine whether findings are exploitable in real-world conditions.

---

## Features

- Semgrep JSON parsing
- AI-powered vulnerability triage
- False positive reduction
- Repository context analysis
- Multi-language support
- Automatic framework detection
- Ollama integration
- Developer remediation recommendations
- Security-focused reasoning
- JSON-based results

---

## Supported Languages

- Python
- Java
- C#
- JavaScript
- TypeScript
- Go
- PHP
- Ruby

---

## Supported Frameworks

- Express
- NestJS
- FastAPI
- Flask
- Django
- Spring Boot
- ASP.NET Core
- Gin
- Echo
- Laravel
- Symfony
- Ruby on Rails

---

## Architecture

```text
Semgrep Report
      |
      v
Semgrep Parser
      |
      v
Technology Detection
      |
      v
Repository Context Builder
      |
      v
Prompt Builder
      |
      v
Ollama
      |
      v
Triage Agent
      |
      v
JSON Classification
```

---

## AI Requirements

AI-Triage uses Ollama as the local LLM runtime.

### Install Ollama

Download and install Ollama:

```text
https://ollama.com
```

### Verify Installation

```bash
ollama list
```

### Download a Model

Recommended:

```bash
ollama pull llama3.1
```

Alternative models:

```bash
ollama pull llama3.2:3b
```

```bash
ollama pull qwen2.5-coder:7b
```

```bash
ollama pull deepseek-coder:6.7b
```

### Test Ollama

```bash
ollama run llama3.1
```

Example:

```text
What is SQL Injection?
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/uelingtonelias/appsec-triage-ai.git
```

```bash
cd ai-triage
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```cmd
.venv\Scripts\activate
```

### Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Install and Run Semgrep

Install Semgrep:

```bash
pip install semgrep
```

Verify installation:

```bash
semgrep --version
```

Run a scan against a repository:

```bash
semgrep scan \
    --config auto \
    --json \
    --output semgrep-report.json \
    ./source
```

Run a security-focused scan:

```bash
semgrep scan \
    --config p/security-audit \
    --json \
    --output semgrep-report.json \
    ./source
```

The generated JSON report will be used by AI-Triage.

---

## Prompt Files

The repository contains two prompt files:

```text
prompt-template.txt
last-prompt.txt
```

### prompt-template.txt

Stores the original prompt template and should be preserved as a reference.

### last-prompt.txt

Stores the most recent prompt sent to the LLM.

Before running the application for the first time, create a copy:

### Windows

```cmd
copy prompt-template.txt last-prompt.txt
```

### Linux

```bash
cp prompt-template.txt last-prompt.txt
```

The application updates `last-prompt.txt` during execution and uses it for troubleshooting and debugging.

---

## Usage

Analyze a Semgrep report:

```bash
python main.py \
    --report semgrep-report.json \
    --repo ./source \
    --limit 10
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--report` | Path to the Semgrep JSON report |
| `--repo` | Repository root path |
| `--limit` | Maximum number of findings to analyze |

---

## End-to-End Example

Generate a Semgrep report:

```bash
semgrep scan \
    --config auto \
    --json \
    --output juice-shop.json \
    ../juice-shop
```

Analyze the findings with AI-Triage:

```bash
python main.py \
    --report juice-shop.json \
    --repo ../juice-shop \
    --limit 5
```

Workflow:

```text
Repository
    |
    v
Semgrep Scan
    |
    v
JSON Report
    |
    v
AI-Triage
    |
    v
Classification
    |
    v
Developer Guidance
```

---

## Classification Types

AI-Triage classifies findings as:

- True Positive
- Likely True Positive
- Needs Review
- Likely False Positive

---

## Example Output

```json
{
  "classification": "Likely False Positive",
  "confidence": 92,
  "risk": "LOW",
  "reasoning": "Input validation was identified before data reached the sink.",
  "evidence": [
    "ValidationService.validateInput()",
    "Parameterized query detected"
  ],
  "developer_recommendation": "Verify all execution paths use the same validation logic.",
  "recommended_code": ""
}
```

---

## Debugging

During execution, AI-Triage generates:

```text
last-prompt.txt
last-response.txt
```

### last-prompt.txt

Contains the last prompt sent to the LLM.

### last-response.txt

Contains the last response returned by the LLM.

These files can be used to troubleshoot:

- Prompt generation issues
- Model hallucinations
- Response formatting issues
- JSON parsing failures
- Context generation problems

---

## Current Roadmap

### Completed

- Semgrep integration
- Ollama integration
- Language detection
- Framework detection
- JSON output parsing
- Prompt generation
- Repository context loading

### Planned

- Context Builder
- Tree-Sitter integration
- Dataflow analysis
- Repository RAG
- DefectDojo integration
- Reviewer Agent
- SARIF support
- CodeQL support
- Snyk support
- Checkmarx support

---

## Project Goal

The primary goal of AI-Triage is to reduce the amount of manual effort required to review SAST findings while maintaining a strong focus on evidence-based security analysis.

AI-Triage does not automatically modify source code.

The tool may recommend secure implementation alternatives and remediation examples, but all remediation decisions remain under developer control.

---

## Disclaimer

AI-Triage provides AI-assisted security analysis.

All findings should be reviewed by qualified security professionals before making remediation, risk acceptance, or risk treatment decisions.

The generated classifications are recommendations and should not be treated as authoritative security determinations.