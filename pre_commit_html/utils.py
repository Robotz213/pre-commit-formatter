"""Utility functions for generating file editor links.

This module provides functionality for constructing URLs that open files in various
editors. It supports multiple editor URL schemes.
"""

import pathlib
from urllib.parse import quote


def generate_editor_links(path: str, line: int = None, column: int = None) -> dict[str, str]:
    """Generate multiple editor links for opening files.

    Args:
        path (str): The file path.
        line (int, optional): The line number in the file.
        column (int, optional): The column number in the file.

    Returns:
        dict[str, str]: A dictionary containing editor-specific URL schemes.

    """
    file_path = pathlib.Path(path).resolve()
    file_uri = file_path.as_uri()  # file:// format
    escaped_path = quote(str(file_path))  # For editors like VS Code, JetBrains, Sublime, Atom, etc.

    # Formatted line and column strings
    line_str = f":{line}" if line else ""
    column_str = f":{column}" if column else ""

    # Editor-specific URL formats
    links = {
        "file://": f"{file_uri}{f'#L{line}' if line else ''}{f'C{column}' if column else ''}",
        "VS Code": f"vscode://file/{escaped_path}{line_str}{column_str}",
        "Nova (macOS)": (
            f"nova://open?path={escaped_path}{f'&line={line}' if line else ''}{f'&column={column}' if column else ''}"
        ),
        "Sublime Text": (
            f"subl://open?url=file://{escaped_path}"
            f"{f'&line={line}' if line else ''}"
            f"{f'&column={column}' if column else ''}"
        ),
        "Atom": (
            f"atom://core/open/file?filename={escaped_path}"
            f"{f'&line={line}' if line else ''}"
            f"{f'&column={column}' if column else ''}"
        ),
        "BBEdit (macOS)": f"bbedit://open?path={escaped_path}{f'&line={line}' if line else ''}",
        "Vim/Nvim": f"vim://open?url=file://{escaped_path}{f'&line={line}' if line else ''}",
    }

    return links
