"""Main module for the pre-commit-html package."""

import argparse
import sys
from typing import Sequence

from pre_commit_html import PreCommitToHTML


def main(argv: Sequence[str] | None = None) -> None:
    """Run the pre-commit formatter."""
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="pre-commit-html")

    parser.add_argument(
        "-i",
        "--IDE",
        type=str,
        help="""IDE for config link files. Supported IDEs: VS Code, Sublime Text, Atom, PyCharm, IntelliJ IDEA, and
                     WebStorm""",
        default="VS Code",
    )
    parser.add_argument("-m", "--to-markdown", "--md", help="Convert the HTML file to Markdown.", action="store_true")
    args = parser.parse_args(argv)
    PreCommitToHTML(
        ide=args.IDE,
        to_markdown=args.to_markdown,
    )
