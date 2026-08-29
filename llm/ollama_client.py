import json
import requests

class OllamaClient:
    def __init__(
        self,
        model="llama3.1:latest"
    ):
        self.model = model
    def ask(self, prompt):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        print("\n========================")
        print("HTTP STATUS")
        print("========================")
        print(response.status_code)

        print("\n========================")
        print("RAW RESPONSE")
        print("========================")
        print(response.text)

        data = response.json()

        if "response" not in data:

            raise RuntimeError(
                f"Unexpected Ollama response:\n"
                f"{json.dumps(data, indent=2)}"
            )

        return data.get("response", "")