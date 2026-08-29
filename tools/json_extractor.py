import json
import re


class JsonExtractor:

    @staticmethod
    def extract(text):

        text = text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if not match:
            return None

        try:

            return json.loads(
                match.group(0)
            )

        except Exception:

            return None