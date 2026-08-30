import requests


class DefectDojoApi:

    def __init__(
        self,
        url: str,
        token: str
    ):

        self.base_url = url.rstrip("/")

        self.headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }

    # ==================================================
    # Products
    # ==================================================

    def get_product_by_name(
        self,
        product_name: str
    ):

        response = requests.get(
            f"{self.base_url}/api/v2/products/",
            params={
                "name": product_name
            },
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if data["count"] == 0:

            return None

        return data["results"][0]

    # ==================================================
    # Engagements
    # ==================================================

    def get_engagements(
        self,
        product_id: int
    ):

        response = requests.get(
            f"{self.base_url}/api/v2/engagements/",
            params={
                "product": product_id
            },
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()["results"]

    def get_engagement_by_name(
        self,
        product_id: int,
        engagement_name: str
    ):

        engagements = self.get_engagements(
            product_id
        )

        for engagement in engagements:

            if (
                engagement["name"].lower()
                == engagement_name.lower()
            ):

                return engagement

        return None

    # ==================================================
    # Tests
    # ==================================================

    def get_tests(
        self,
        engagement_id: int
    ):

        response = requests.get(
            f"{self.base_url}/api/v2/tests/",
            params={
                "engagement": engagement_id
            },
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()["results"]

    def get_semgrep_test(
        self,
        engagement_id: int
    ):

        tests = self.get_tests(
            engagement_id
        )

        for test in tests:

            if (
                test.get(
                    "test_type_name",
                    ""
                )
                == "Semgrep JSON Report"
            ):

                return test

        return None

    # ==================================================
    # Finding Discovery
    # ==================================================

    def get_findings(
        self,
        test_id: int,
        limit: int = 500
    ):

        response = requests.get(
            f"{self.base_url}/api/v2/findings/",
            params={
                "test": test_id,
                "limit": limit
            },
            headers=self.headers,
            timeout=60
        )

        response.raise_for_status()

        return response.json()["results"]

    def find_finding(
        self,
        test_id: int,
        rule_id: str,
        file_path: str = None,
        line: int = None
    ):

        findings = self.get_findings(
            test_id
        )

        for finding in findings:

            vuln_id = finding.get(
                "vuln_id_from_tool"
            )

            if vuln_id != rule_id:

                continue

            if file_path:

                dojo_file = (
                    finding.get(
                        "file_path"
                    )
                    or ""
                )

                if dojo_file != file_path:

                    continue

            if line:

                dojo_line = (
                    finding.get(
                        "line"
                    )
                    or 0
                )

                if dojo_line != line:

                    continue

            return finding

        return None

    # ==================================================
    # Finding Update
    # ==================================================

    def update_finding(
        self,
        finding_id: int,
        result: dict
    ):

        classification = result.get(
            "classification",
            "Needs Review"
        )

        verified = False
        false_positive = False
        under_review = False

        if (
            classification
            == "True Positive"
        ):

            verified = True

        elif (
            classification
            == "Likely True Positive"
        ):

            verified = True

        elif (
            classification
            == "Likely False Positive"
        ):

            false_positive = True

        else:

            under_review = True

        severity_justification = (
            f"AI-Triage Classification: "
            f"{classification}\n\n"
            f"Confidence: "
            f"{result.get('confidence', 0)}\n\n"
            f"Risk: "
            f"{result.get('risk', 'UNKNOWN')}\n\n"
            f"Reasoning:\n"
            f"{result.get('reasoning', '')}"
        )

        mitigation = result.get(
            "developer_recommendation",
            ""
        )

        current = requests.get(
            f"{self.base_url}/api/v2/findings/{finding_id}/",
            headers=self.headers,
            timeout=30
        )

        current.raise_for_status()

        current_finding = current.json()

        tags = current_finding.get(
            "tags",
            []
        )

        if "AI-Triage" not in tags:

            tags.append(
                "AI-Triage"
            )

        classification_tag = (
            classification
            .replace(" ", "-")
        )

        if (
            classification_tag
            not in tags
        ):

            tags.append(
                classification_tag
            )

        payload = {
            "verified": verified,
            "false_p": false_positive,
            "under_review": under_review,
            "severity_justification":
                severity_justification,
            "mitigation": mitigation,
            "tags": tags
        }

        response = requests.patch(
            f"{self.base_url}/api/v2/findings/{finding_id}/",
            headers=self.headers,
            json=payload,
            timeout=30
        )

        if not response.ok:

            print(
                "[ERROR] Failed to "
                "update finding:"
            )

            print(
                response.text
            )

        response.raise_for_status()

        return response.json()

    # ==================================================
    # Product / Engagement /
    # Semgrep Test Discovery
    # ==================================================

    # ==================================================
# Product / Semgrep Test Discovery
# ==================================================

    def get_latest_semgrep_test(
        self,
        product_id: int
    ):

        engagements = self.get_engagements(
            product_id
        )

        for engagement in engagements:

            semgrep_test = (
                self.get_semgrep_test(
                    engagement["id"]
                )
            )

            if semgrep_test:

                return {
                    "engagement_id": (
                        engagement["id"]
                    ),
                    "test_id": (
                        semgrep_test["id"]
                    )
                }

        return None


    def get_product_and_semgrep_test(
        self,
        product_name: str
        ):

        product = self.get_product_by_name(
            product_name
        )

        if not product:

            raise RuntimeError(
                f"Product not found: "
                f"{product_name}"
            )

        semgrep = (
            self.get_latest_semgrep_test(
                product["id"]
            )
        )

        if not semgrep:

            raise RuntimeError(
                "Semgrep JSON Report "
                "test not found."
            )

        return {
            "product_id":
                product["id"],

            "engagement_id":
                semgrep[
                    "engagement_id"
                ],

            "test_id":
                semgrep[
                    "test_id"
                ]
            }
    # ==================================================
    # AI Triage Review
    # ==================================================

    def append_ai_triage_review(
        self,
        test_id: int,
        rule_id: str,
        file_path: str,
        line: int,
        result: dict
    ):

        finding = self.find_finding(
            test_id=test_id,
            rule_id=rule_id,
            file_path=file_path,
            line=line
        )

        if not finding:

            print(
                "[WARN] Matching "
                "finding not found "
                "in DefectDojo."
            )

            return False

        self.update_finding(
            finding_id=finding["id"],
            result=result
        )

        return True