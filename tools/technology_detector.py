from pathlib import Path
import json

class TechnologyDetector:
    def detect(self, repo_path: str) -> dict:
        return {
            "language": self.detect_language(repo_path),
            "framework": self.detect_framework(repo_path)
        }

    def detect_language(self, repo_path: str) -> str:

        repo = Path(repo_path)

        counters = {
            "Python": 0,
            "JavaScript": 0,
            "TypeScript": 0,
            "Java": 0,
            "C#": 0,
            "Go": 0,
            "PHP": 0,
            "Ruby": 0,
            "Rust": 0
        }

        extension_map = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".cs": "C#",
            ".go": "Go",
            ".php": "PHP",
            ".rb": "Ruby",
            ".rs": "Rust"
        }

        for file in repo.rglob("*"):

            if not file.is_file():
                continue

            language = extension_map.get(file.suffix)

            if language:
                counters[language] += 1

        winner = max(counters, key=counters.get)

        if counters[winner] == 0:
            return "Unknown"

        return winner

    def detect_framework(self, repo_path: str) -> str:

        repo = Path(repo_path)

        #
        # JavaScript / TypeScript
        #
        package_json = repo / "package.json"

        if package_json.exists():

            try:

                data = json.loads(
                    package_json.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                )

                deps = {}
                deps.update(data.get("dependencies", {}))
                deps.update(data.get("devDependencies", {}))

                if "express" in deps:
                    return "Express"

                if "@nestjs/core" in deps:
                    return "NestJS"

                if "next" in deps:
                    return "Next.js"

                if "react" in deps:
                    return "React"

                if "vue" in deps:
                    return "Vue"

                if "@angular/core" in deps:
                    return "Angular"

            except Exception:
                pass

        #
        # Python
        #
        requirements_txt = repo / "requirements.txt"

        if requirements_txt.exists():

            text = requirements_txt.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "fastapi" in text:
                return "FastAPI"

            if "django" in text:
                return "Django"

            if "flask" in text:
                return "Flask"

        pyproject_toml = repo / "pyproject.toml"

        if pyproject_toml.exists():

            text = pyproject_toml.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "fastapi" in text:
                return "FastAPI"

            if "django" in text:
                return "Django"

            if "flask" in text:
                return "Flask"

        #
        # Java
        #
        pom_xml = repo / "pom.xml"

        if pom_xml.exists():

            text = pom_xml.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "spring-boot" in text:
                return "Spring Boot"

        build_gradle = repo / "build.gradle"

        if build_gradle.exists():

            text = build_gradle.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "spring-boot" in text:
                return "Spring Boot"

        #
        # .NET
        #
        for csproj in repo.rglob("*.csproj"):

            try:

                text = csproj.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if "Microsoft.AspNetCore" in text:
                    return "ASP.NET Core"

            except Exception:
                continue

        #
        # Go
        #
        go_mod = repo / "go.mod"

        if go_mod.exists():

            text = go_mod.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "gin-gonic" in text:
                return "Gin"

            if "labstack/echo" in text:
                return "Echo"

        #
        # PHP
        #
        composer_json = repo / "composer.json"

        if composer_json.exists():

            try:

                data = json.loads(
                    composer_json.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                )

                deps = data.get("require", {})

                if "laravel/framework" in deps:
                    return "Laravel"

                if "symfony/framework-bundle" in deps:
                    return "Symfony"

            except Exception:
                pass

        #
        # Ruby
        #
        gemfile = repo / "Gemfile"

        if gemfile.exists():

            text = gemfile.read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "rails" in text:
                return "Ruby on Rails"

        return "Unknown"