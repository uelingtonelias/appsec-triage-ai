from pathlib import Path


class ContextBuilder:
    def build(
        self,
        repo_path: str,
        finding,
        lines_before: int = 20,
        lines_after: int = 20
    ) -> str:
        try:
            file_path = Path(
                finding.file_path
            )
            if not file_path.is_absolute():

                file_path = (
                    Path(repo_path)
                    / finding.file_path
                )
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
            lines = content.splitlines()
            start_line = max(
                1,
                getattr(
                    finding,
                    "start_line",
                    1
                )
            )
            end_line = max(
                start_line,
                getattr(
                    finding,
                    "end_line",
                    start_line
                )
            )
            context_start = max(
                0,
                start_line - lines_before - 1
            )
            context_end = min(
                len(lines),
                end_line + lines_after
            )
            context_lines = []
            for line_number in range(
                context_start,
                context_end
            ):
                prefix = " "
                if (
                    start_line - 1
                    <= line_number
                    <= end_line - 1
                ):
                    prefix = ">"
                context_lines.append(
                    f"{prefix} "
                    f"{line_number + 1:05d}: "
                    f"{lines[line_number]}"
                )
            return "\n".join(
                context_lines
            )
        except Exception as ex:
            print(
                f"[WARN] ContextBuilder failed: "
                f"{ex}"
            )
            return ""