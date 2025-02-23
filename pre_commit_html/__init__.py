"""Module for formatting pre-commit results into an HTML file."""

import os
import subprocess
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

result_html = Path("result_pre_commit.html")
result_md = Path("result_pre_commit.md")


class PreCommitToHTML:
    """Class to parse and format pre-commit results.

    Attributes:
        code_error (list[str]): Represents the section where the linter
            error is occurring with:
            - File path
            - Line number
            - Column number
            - Error message

        code_part (list[str]): Represents the code part where the linter
        html_content (list[str]): Represents the HTML content to be written to the file.

    """

    ide = "VS Code"
    to_markdown = False
    code_error: list[str | list[str]] = []
    code_part: list[str] = []
    html_content: list[list[str | list[str]]] = []

    def __init__(self, ide: str = "VS Code", to_markdown: bool = False) -> None:
        """Initialize the PreCommitToHTML class."""
        self.ide = ide
        self.to_markdown = to_markdown
        self.pre_commit_html()

    def render_template(self) -> None:
        """Render the template and write the result to an HTML file."""
        html_content = render_template("html_content.jinja").render(content_list=self.html_content)
        if result_html.exists():
            os.remove(str(result_html))

        with result_html.open("w", encoding="utf-8") as f:
            f.write(html_content)

        if self.to_markdown:
            with result_md.open("w", encoding="utf-8") as f:
                from docling.document_converter import DocumentConverter

                result = DocumentConverter().convert(result_html).document.export_to_markdown()
                f.write(result)

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

    def format_result(self, h3_file: str) -> None:
        """Format the error head message."""
        path_code_file = h3_file.split(":")[0]
        line_code = h3_file.split(":")[1]
        column_code = h3_file.split(":")[2]
        message = h3_file.split(":")[3]
        path_file_link = str(path_code_file)
        ruff_ref = message.split(" ")[1]

        try:
            workdir = Path.cwd().resolve()
            path_code_file = h3_file.split(":")[0]

            path_file_link = generate_editor_links(
                workdir.joinpath(str(path_code_file)), int(line_code), int(column_code)
            )[self.ide]
        except Exception as e:
            print(  # noqa:T201
                f"""
                ====================================
                Error to generate link to file editor
                File: {path_code_file}
                Exception: {e}
                ====================================
                """
            )

        ruff_ref = message.split(" ")[1]

        self.code_error.append(
            "".join((
                f'<h3>File: <a href="{path_file_link}',
                f'{column_code}">{path_code_file}:{line_code}:{column_code}</a></h3>',
            ))
        )
        self.code_error.append(
            f'<p>Error: <a href="https://docs.astral.sh/ruff/rules/#{ruff_ref}">{ruff_ref}</a>{message}</p>'
        )

    def pre_commit_html(self) -> None:
        """Format the pre-commit output into an HTML file.

        This method runs the pre-commit command, processes its output, and writes the formatted
        results into an HTML file.
        """
        content = self.run_pre_commit()

        content_splitlines = content.splitlines()

        for line in content_splitlines:
            if "\\" in line and ":" in line and len(self.code_part) == 0:
                # if a file is found, add it to the code_part list if it is empty
                h3_file = line.replace("\\", "/")

                if len(h3_file.split(":")) == 4:
                    self.format_result(h3_file=h3_file)

            elif "\\" in line and ":" in line and len(self.code_part) > 0:
                # else, if another file is found, clear the code_part list
                # and add the previous file to the html_content list

                self.code_error.append(self.code_part)
                self.html_content.append(self.code_error)

                h3_file = line.replace("\\", "/")
                if len(h3_file.split(":")) == 4:
                    self.format_result(h3_file=h3_file)

                continue

            if "|" in line:
                self.code_part.append(line.replace("|", ""))

        self.render_template()
