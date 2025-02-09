"""This module contains the main function to run the pre-commit formatter."""

from . import PreCommitParser


def main() -> None:
    """Main function to run the pre-commit formatter.

    This function calls the pre_commit_html method from the PreCommitParser class.
    """
    PreCommitParser.pre_commit_html()
