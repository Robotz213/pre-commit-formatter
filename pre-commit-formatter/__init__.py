""" "Module for formatting pre-commit result into html file."""

from html.parser import HTMLParser  # noqa: F401
from pathlib import Path

from jinja2 import Template, Environment, FileSystemLoader  # noqa: F401

"""
<li>
    <h3> File: <a href="./"></a></h3>
    <p>Error: </p>

    <p>Line: </p>

</li>



"""
env = Environment(
    loader=FileSystemLoader(Path(__file__).parent.resolve().joinpath("site/templates"))
)

render_template = env.get_template

path_result_content = Path("result_pre_commit.html")


def pre_commit_formatter():
    with open("pre-commit_result.txt", "r", encoding="utf-8") as f:
        content = f.read()

        # html_content =

        content_splitlines = content.splitlines()

        html_content: list[str] = []

        code_part: list[str] = []

        code_error: list[str] = []

        for line in content_splitlines:
            if "\\" in line and ":" in line and len(code_part) == 0:
                h3_file = line.replace("\\", "/")

                path_code_file = h3_file.split(":")[0]
                line_code = h3_file.split(":")[1]
                column_code = h3_file.split(":")[2]
                message = h3_file.split(":")[3]

                ruff_ref = message.split(" ")[1]

                code_error.append(
                    "".join(
                        (
                            f'<h3>File: <a href="./{path_code_file}:{line_code}:',
                            f'{column_code}">{path_code_file}:{line_code}:{column_code}</a></h3>',
                        )
                    )
                )
                code_error.append(
                    f'<p>Error: <a href="https://docs.astral.sh/ruff/rules/#{ruff_ref}"></a>{message}</p>'
                )

            elif "\\" in line and ":" in line and len(code_part) > 0:
                h3_file = line.replace("\\", "/")

                code_part_html = render_template("code_part.jinja").render(
                    code_part=code_part
                )

                code_error.append(code_part_html)
                to_html = render_template("code_error.jinja").render(
                    code_error=code_error
                )

                html_content.append(to_html)

                code_part.clear()
                code_error.clear()

                path_code_file = h3_file.split(":")[0]
                line_code = h3_file.split(":")[1]
                column_code = h3_file.split(":")[2]
                message = h3_file.split(":")[3]

                ruff_ref = message.split(" ")[1]

                code_error.append(
                    "".join(
                        (
                            f'<h3>File: <a href="./{path_code_file}:{line_code}:',
                            f'{column_code}">{path_code_file}:{line_code}:{column_code}</a></h3>',
                        )
                    )
                )
                code_error.append(
                    f'<p>Error: <a href="https://docs.astral.sh/ruff/rules/#{ruff_ref}"></a>{message}</p>'
                )
                continue

            if "|" in line:
                code_part.append(line)

        if path_result_content.exists():
            path_result_content.unlink()

        path_result_content.touch()

        html_content = render_template("html_content.jinja").render(
            content=html_content
        )

        with open(path_result_content, "w", encoding="utf-8") as f:
            f.write(html_content)


pre_commit_formatter()
