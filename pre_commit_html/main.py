"""Main module for the pre-commit-html package."""

import argparse
import sys
from typing import Sequence

from pre_commit_html import PreCommitToHTML


def main(argv: Sequence[str] | None = None) -> None:
    """Run the pre-commit formatter."""
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="pre-commit-html")

    parser.add_argument("-i", "--IDE", type=str, help="The IDE to open the file in.", default="VS Code")

    args = parser.parse_args(argv)
    PreCommitToHTML(ide=args.IDE)
