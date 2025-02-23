"""Module for formatting pre-commit results into an HTML file."""

import os
import subprocess
from pathlib import Path

import html2text
import yaml  # noqa: F401
from jinja2 import Environment, FileSystemLoader

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

    theme = "dark"
    ide = "VS Code"
    to_markdown = False
    code_error: list[str | list[str]] = []
    code_part: list[str] = []
    html_content: list[list[str | list[str]]] = []

    uri_html = ""

    def __init__(self, ide: str = "VS Code", to_markdown: bool = False, theme: str = "dark") -> None:
        """Initialize the PreCommitToHTML class."""
        self.ide = ide
        self.to_markdown = to_markdown
        self.theme = theme
        self.pre_commit_html()

    def render_template(self) -> None:
        """Render the template and write the result to an HTML file."""
        html_content = render_template("html_content.jinja").render(
            content=self.html_content,
            theme=self.theme,
            errors=len(self.html_content),
        )
        if result_html.exists():
            os.remove(str(result_html))

        with result_html.open("w", encoding="utf-8") as f:
            f.write(html_content)

        if self.to_markdown:
            try:
                converter = html2text.HTML2Text()
                converter.body_width = 0
                converter.code = True

                with result_md.open("w", encoding="utf-8") as f:
                    result = converter.handle(html_content)
                    f.write(result)

            except ImportError:
                print(  # noqa:T201
                    """
                    ====================================
                    Docling package is required to convert HTML to Markdown.
                    Please install it using the following command:
                    `pip install docling` or poetry add docling
                    ====================================
                    """
                )

    def run_pre_commit(self) -> str:
        """Run the pre-commit command and capture its output.

        Returns:
            str: The output of the pre-commit command.

        Raises:
            subprocess.CalledProcessError: If the pre-commit command fails.

        """
        try:
            results = ""
            yaml_config = yaml.safe_load(Path(".pre-commit-config.yaml").read_text())
            repos = yaml_config.get("repos")
            for repo in repos:
                hooks = repo.get("hooks")
                for hook in hooks:
                    id_hook = hook.get("id")
                    if id_hook:
                        command = ["pre-commit", "run", id_hook, "--all-files"]
                        if id_hook == "bandit":
                            command.append("--verbose")
                        result = subprocess.run(
                            command,
                            capture_output=True,
                            text=True,
                            cwd=str(Path(__file__).cwd()),
                            encoding="utf-8",
                        )

                        if result.stdout:
                            if "Failed" in result.stdout:
                                if results != "":
                                    results += f"{result.stdout}\n"
                                    continue

                                results = result.stdout
            return results
        except subprocess.CalledProcessError as e:
            return f"Erro ao executar pre-commit: {e.stderr}"

    def format_result(self, h3_file: str) -> None:
        """Format the error head message."""
        ruff_ref = ""
        path_code_file = h3_file.split(":")[0]
        line_code = h3_file.split(":")[1]
        column_code = h3_file.split(":")[2]
        message = h3_file.split(":")[3]
        path_file_link = str(path_code_file)

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
        self.code_error.append(message)
        self.code_error.append(f"{path_code_file}:{line_code}:{column_code}")
        self.code_error.append(path_file_link)
        if len(message.split(" ")) > 1:
            ruff_ref = message.split(" ")[1]
            self.code_error.append(f"https://docs.astral.sh/ruff/rules/#{ruff_ref}")

        else:
            self.code_error.append("")

    def pre_commit_html(self) -> None:
        """Format the pre-commit output into an HTML file.

        This method runs the pre-commit command, processes its output, and writes the formatted
        results into an HTML file.
        """
        content = self.run_pre_commit()

        content_splitlines = content.splitlines()

        for line in content_splitlines:
            if "\\" in line and ":" in line:
                if "|" in line:
                    continue
                # if a file is found, add it to the code_part list if it is empty
                h3_file = line.replace("\\", "/")

                if len(self.code_part) > 0 or len(self.code_error) > 0:
                    self.code_error.append(self.code_part)
                    to_append = self.code_error
                    self.html_content.append(to_append)

                    self.code_error = []
                    self.code_part = []

                if len(h3_file.split(":")) > 3:
                    self.format_result(h3_file=h3_file)

                continue

            if "|" in line:
                code_content = line
                if code_content.strip() == "|":
                    continue
                self.code_part.append(code_content)

        if all(
            [  # noqa:W503
                len(self.html_content) == 0,
                len(self.code_part) > 0,
                len(self.code_error) > 0,
            ],
        ):
            self.code_error.append(self.code_part)
            self.html_content.append(self.code_error)

            h3_file = line.replace("\\", "/")
            if len(h3_file.split(":")) == 4:
                self.format_result(h3_file=h3_file)

        self.render_template()
        self.uri_html = result_html.resolve().as_uri()
        print(f"HTML file generated: {self.uri_html}")  # noqa:T201
