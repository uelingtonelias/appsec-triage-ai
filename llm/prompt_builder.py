from pathlib import Path


class PromptBuilder:

    def __init__(self):

        self.system_prompt = Path(
            "prompts/system_prompt.txt"
        ).read_text(
            encoding="utf-8"
        )

    def build(
        self,
        finding,
        context
    ):

        prompt = self.system_prompt

        prompt = prompt.replace(
            "{language}",
            context.language
        )

        prompt = prompt.replace(
            "{framework}",
            context.framework
        )

        prompt += self._technology_guidance(
            finding,
            context
        )

        prompt += f"""

FINDING ANALYSIS
================

Language:
{context.language}

Framework:
{context.framework}

Finding Information
===================

Rule ID:
{finding.rule_id}

Severity:
{finding.severity}

Message:
{finding.message}

File:
{finding.file_path}

Start Line:
{finding.start_line}

End Line:
{finding.end_line}

Affected Code
=============

{finding.code_snippet}

Dataflow Information
====================

Source:
{finding.source}

Intermediate Flow:
{finding.dataflow}

Sink:
{finding.sink}

Repository Context
==================

{context.file_content}

Related Files
=============

{chr(10).join(context.related_files)}

Analysis Tasks
==============

Perform a security review of this finding and determine:

1. Whether user-controlled input exists.
2. Whether the source can realistically reach the reported sink.
3. Whether sanitization or validation controls exist.
4. Whether framework protections mitigate the issue.
5. Whether authentication or authorization controls impact exploitability.
6. Whether the vulnerable code path is realistically reachable.
7. Whether exploitation is feasible in a real-world attack scenario.
8. Whether the finding is:

   - True Positive
   - Likely True Positive
   - Needs Review
   - Likely False Positive

Return ONLY valid JSON.
"""

        return prompt

    def _technology_guidance(
        self,
        finding,
        context
    ):

        rule_id = (
            finding.rule_id or ""
        ).lower()

        file_path = (
            finding.file_path or ""
        ).lower()

        file_content = (
            context.file_content or ""
        ).lower()

        #
        # GitHub Actions
        #
        if (
            "github-actions" in rule_id
            or "/.github/workflows/" in file_path
            or "\\.github\\workflows\\" in file_path
        ):
            return self._github_actions_guidance()

        #
        # GitLab CI
        #
        if (
            "gitlab" in rule_id
            or ".gitlab-ci.yml" in file_path
        ):
            return self._gitlab_guidance()

        #
        # Azure DevOps
        #
        if (
            "azure-devops" in rule_id
            or "azure-pipelines.yml" in file_path
            or "azure-pipelines.yaml" in file_path
        ):
            return self._azure_devops_guidance()

        #
        # Terraform
        #
        if (
            "terraform" in rule_id
            or file_path.endswith(".tf")
        ):
            return self._terraform_guidance()

        #
        # Docker
        #
        if (
            "docker" in rule_id
            or "dockerfile" in file_path
            or "docker-compose.yml" in file_path
            or "docker-compose.yaml" in file_path
        ):
            return self._docker_guidance()

        #
        # Kubernetes
        #
        if (
            "kubernetes" in rule_id
            or "k8s" in rule_id
            or (
                "apiversion:" in file_content
                and "kind:" in file_content
            )
        ):
            return self._kubernetes_guidance()

        return ""

    def _github_actions_guidance(self):

        return """

==================================================
GITHUB ACTIONS SECURITY GUIDANCE
==================================================

For GitHub Actions findings:

Do not require source-to-sink analysis.

Do not require user-controlled input.

Evaluate:

- Supply chain risk
- Pipeline compromise risk
- Dependency trust
- Workflow integrity
- Execution of untrusted code
- Mutable action references
- Secret exposure

Mutable references:

Less secure:

uses: actions/checkout@v4

Preferred:

uses: actions/checkout@<full_commit_sha>

For curl | bash patterns:

Treat findings as high confidence when remote content is downloaded and immediately executed without integrity verification.

For GitHub Actions findings, traditional dataflow analysis may not apply.
"""

    def _gitlab_guidance(self):

        return """

==================================================
GITLAB CI SECURITY GUIDANCE
==================================================

For GitLab CI findings evaluate:

- Pipeline security
- Supply chain risk
- Secret exposure
- Unsafe script execution
- Dependency trust

Do not require traditional source-to-sink analysis.

Focus on CI/CD security impact.
"""

    def _azure_devops_guidance(self):

        return """

==================================================
AZURE DEVOPS SECURITY GUIDANCE
==================================================

For Azure DevOps findings evaluate:

- Pipeline security
- Secret exposure
- Dependency trust
- Unsafe script execution
- Privileged build agents

Do not require traditional source-to-sink analysis.

Focus on CI/CD infrastructure risk.
"""

    def _terraform_guidance(self):

        return """

==================================================
TERRAFORM SECURITY GUIDANCE
==================================================

For Terraform findings evaluate:

- Public cloud exposure
- Open security groups
- Excessive IAM permissions
- Secret exposure
- Weak encryption settings
- Public storage

Do not require traditional application dataflow analysis.

Focus on infrastructure risk.
"""

    def _docker_guidance(self):

        return """

==================================================
DOCKER SECURITY GUIDANCE
==================================================

For Docker findings evaluate:

- Root containers
- Privileged execution
- Container breakout risk
- Weak base images
- Secret leakage
- Sensitive file exposure

Do not require traditional source-to-sink analysis.

Focus on container security posture.
"""

    def _kubernetes_guidance(self):

        return """

==================================================
KUBERNETES SECURITY GUIDANCE
==================================================

For Kubernetes findings evaluate:

- Privileged containers
- HostPath mounts
- Host network access
- Host PID access
- Excessive RBAC permissions
- Service account misuse
- Secret exposure
- Image trust

Do not require traditional source-to-sink analysis.

Focus on cluster security impact and configuration risk.
"""