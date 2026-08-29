import json
import time
import requests


SEPARATOR = "=" * 40

DEFAULT_CLASSIFICATION = "Needs Review"
DEFAULT_RISK = "LOW"


TRIAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "classification": {
            "type": "string",
            "enum": [
                "True Positive",
                "Likely True Positive",
                "Needs Review",
                "Likely False Positive"
            ]
        },
        "confidence": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
        },
        "risk": {
            "type": "string",
            "enum": [
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ]
        },
        "reasoning": {
            "type": "string"
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "developer_recommendation": {
            "type": "string"
        },
        "recommended_code": {
            "type": "string"
        }
    },
    "required": [
        "classification",
        "confidence",
        "risk",
        "reasoning",
        "evidence",
        "developer_recommendation",
        "recommended_code"
    ]
}


class OllamaClient:

    DEFAULT_RESULT = {
        "classification": DEFAULT_CLASSIFICATION,
        "confidence": 0,
        "risk": DEFAULT_RISK,
        "reasoning": "",
        "evidence": [],
        "developer_recommendation": "",
        "recommended_code": ""
    }

    VALID_CLASSIFICATIONS = {
        "True Positive",
        "Likely True Positive",
        DEFAULT_CLASSIFICATION,
        "Likely False Positive"
    }

    VALID_RISKS = {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    }

    def __init__(
        self,
        model="qwen2.5-coder:7b",
        timeout=900
    ):
        self.model = model
        self.timeout = timeout

    def ask(self, prompt):

        print(f"\n{SEPARATOR}")
        print("OLLAMA REQUEST")
        print(SEPARATOR)
        print(f"Model: {self.model}")
        print(f"Prompt Size: {len(prompt)} chars")

        start_time = time.time()

        try:

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": TRIAGE_SCHEMA,
                    "options": {
                        "temperature": 0,
                        "num_predict": 400,
                        "num_ctx": 8192
                    }
                },
                timeout=self.timeout
            )

            if response.status_code != 200:

                print(f"\n{SEPARATOR}")
                print("OLLAMA ERROR")
                print(SEPARATOR)
                print(response.text)

            response.raise_for_status()

        except requests.exceptions.Timeout:

            raise RuntimeError(
                f"Ollama timeout after {self.timeout} seconds"
            )

        except requests.exceptions.RequestException as ex:

            raise RuntimeError(
                f"Ollama communication error: {ex}"
            )

        elapsed = time.time() - start_time

        data = response.json()

        prompt_tokens = data.get(
            "prompt_eval_count",
            0
        )

        response_tokens = data.get(
            "eval_count",
            0
        )

        total_tokens = (
            prompt_tokens +
            response_tokens
        )

        print(f"\n{SEPARATOR}")
        print("OLLAMA METRICS")
        print(SEPARATOR)
        print(f"Prompt Tokens    : {prompt_tokens}")
        print(f"Response Tokens  : {response_tokens}")
        print(f"Total Tokens     : {total_tokens}")
        print(f"Elapsed Seconds  : {elapsed:.2f}")

        raw_response = data.get(
            "response",
            ""
        ).strip()

        if not raw_response:

            raise RuntimeError(
                "Ollama returned an empty response"
            )

        print(f"\n{SEPARATOR}")
        print("RAW LLM RESPONSE")
        print(SEPARATOR)
        print(raw_response)

        try:

            result = json.loads(
                raw_response
            )

        except json.JSONDecodeError as ex:

            raise RuntimeError(
                f"Invalid JSON returned by model: {ex}\n\n"
                f"{raw_response}"
            )

        result = self._validate_response(
            result
        )

        return {
            "result": result,
            "metrics": {
                "prompt_tokens": prompt_tokens,
                "response_tokens": response_tokens,
                "total_tokens": total_tokens,
                "elapsed_seconds": elapsed
            }
        }

    def _validate_response(
        self,
        result
    ):

        if not isinstance(
            result,
            dict
        ):
            result = {}

        #
        # Fill missing fields
        #
        for key, value in self.DEFAULT_RESULT.items():

            result.setdefault(
                key,
                value
            )

        #
        # Classification
        #
        if result["classification"] not in self.VALID_CLASSIFICATIONS:

            result["classification"] = (
                DEFAULT_CLASSIFICATION
            )

        #
        # Risk
        #
        if result["risk"] not in self.VALID_RISKS:

            result["risk"] = DEFAULT_RISK

        #
        # Confidence
        #
        try:

            result["confidence"] = int(
                result["confidence"]
            )

        except Exception:

            result["confidence"] = 0

        result["confidence"] = max(
            0,
            min(
                100,
                result["confidence"]
            )
        )

        #
        # Normalize text fields
        #
        for field in [
            "reasoning",
            "developer_recommendation",
            "recommended_code"
        ]:

            if result[field] is None:

                result[field] = ""

            result[field] = str(
                result[field]
            )

        #
        # Normalize evidence
        #
        if not isinstance(
            result["evidence"],
            list
        ):
            result["evidence"] = []

        normalized_evidence = []

        for item in result["evidence"]:

            if isinstance(
                item,
                str
            ):

                normalized_evidence.append(
                    item
                )

            else:

                normalized_evidence.append(
                    json.dumps(
                        item,
                        ensure_ascii=False
                    )
                )

        result["evidence"] = normalized_evidence

        return result