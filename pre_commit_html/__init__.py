"""Module for formatting pre-commit results into an HTML file."""

import subprocess
from contextlib import suppress
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template  # noqa: F401

from pre_commit_html.utils import generate_editor_links

env = Environment(  # noqa:S701
    loader=FileSystemLoader(
        Path(
            __file__,
        )
        .parent.resolve()
        .joinpath("site/templates")
    ),
)

render_template = env.get_template

path_result_content = Path("result_pre_commit.html")


class PreCommitToHTML:
    """Class to parse and format pre-commit results."""

    def __init__(self, ide: str = "VS Code") -> None:
        """Initialize the PreCommitToHTML class."""
        self.ide = ide
        self.pre_commit_html()

    def run_pre_commit(self) -> str:
        """Run the pre-commit command and capture its output.

        Returns:
            str: The output of the pre-commit command.

        Raises:
            subprocess.CalledProcessError: If the pre-commit command fails.

        """
        try:
            result = subprocess.run(
                ["pre-commit", "run", "--all-files"],
                capture_output=True,
                text=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Erro ao executar pre-commit: {e.stderr}"

    def pre_commit_html(self) -> None:
        """Format the pre-commit output into an HTML file.

        This method runs the pre-commit command, processes its output, and writes the formatted
        results into an HTML file.
        """
        content = self.run_pre_commit()

        content_splitlines = content.splitlines()

        html_content: list[str] = []

        code_part: list[str] = []

        code_error: list[str] = []

        for line in content_splitlines:
            if "\\" in line and ":" in line and len(code_part) == 0:
                h3_file = line.replace("\\", "/")

                if len(h3_file.split(":")) == 4:
                    path_code_file = h3_file.split(":")[0]
                    path_file_link = path_code_file

                    line_code = h3_file.split(":")[1]
                    column_code = h3_file.split(":")[2]
                    message = h3_file.split(":")[3]

                    with suppress(Exception):
                        workdir = Path.cwd().resolve()
                        path_code_file = h3_file.split(":")[0]

                        path_file_link = generate_editor_links(
                            workdir.joinpath(str(path_code_file)), int(line_code), int(column_code)
                        )[self.ide]

                    ruff_ref = message.split(" ")[1]

                    code_error.append(
                        "".join((
                            f'<h3>File: <a href="{path_file_link}:{line_code}:',
                            f'{column_code}">{path_code_file}:{line_code}:{column_code}</a></h3>',
                        ))
                    )
                    code_error.append(
                        f'<p>Error: <a href="https://docs.astral.sh/ruff/rules/#{ruff_ref}">{ruff_ref}</a>{message}</p>'
                    )

            elif "\\" in line and ":" in line and len(code_part) > 0:
                h3_file = line.replace("\\", "/")

                code_part_html = render_template("code_part.jinja").render(code_part=code_part)

                code_error.append(code_part_html)
                to_html = render_template("code_error.jinja").render(code_error=code_error)

                html_content.append(to_html)

                code_part.clear()
                code_error.clear()

                path_code_file = h3_file.split(":")[0]
                line_code = h3_file.split(":")[1]
                column_code = h3_file.split(":")[2]
                message = h3_file.split(":")[3]

                ruff_ref = message.split(" ")[1]

                code_error.append(
                    "".join((
                        f'<h3>File: <a href="./{path_code_file}:{line_code}:',
                        f'{column_code}">{path_code_file}:{line_code}:{column_code}</a></h3>',
                    ))
                )
                code_error.append(
                    f'<p>Error: <a href="https://docs.astral.sh/ruff/rules/#{ruff_ref}">{ruff_ref}</a>{message}</p>'
                )
                continue

            if "|" in line:
                code_part.append(line)

        if path_result_content.exists():
            path_result_content.unlink()

        path_result_content.touch()

        html_content = render_template("html_content.jinja").render(content=html_content)

        with open(path_result_content, "w", encoding="utf-8") as f:
            f.write(html_content)
