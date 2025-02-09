# Pre-Commit Formatter

> Portuguese version [here](docs/README-pt.md)(Link only works on the project page).

This project is designed to run pre-commit hooks and format the results into an HTML file for easy viewing.

## Summary

- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Templates](#templates)
- [Example](#example)
- [License](#license)
- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## How It Works

1. **Run Pre-Commit Hooks**: The `PreCommitParser` class runs the pre-commit hooks using the `pre-commit run --all-files` command.
2. **Parse Output**: The output from the pre-commit hooks is parsed to extract relevant information such as file paths, line numbers, column numbers, and error messages.
3. **Generate HTML**: The parsed information is then formatted into an HTML file using Jinja2 templates. The HTML file includes links to the relevant lines in the source code and references to the documentation for the errors.

## Installation

To use this project, you need to have Python and `pre-commit` installed. You can install the required dependencies using pip:

```sh
poetry install
```

## Usage

To run the pre-commit formatter, execute the following command:

```sh
python -m pre_commit_html
```

This will generate an HTML file named `result_pre_commit.html` in the project directory.

## Project Structure

- `pre_commit_html/__main__.py`: Contains the main function to run the pre-commit formatter.
- `pre_commit_html/__init__.py`: Contains the `PreCommitParser` class which handles running the pre-commit hooks and formatting the output.
- `site/templates/`: Contains the Jinja2 templates used to generate the HTML file.

## Templates

The project uses Jinja2 templates to format the HTML output. The templates are located in the `site/templates/` directory and include:

- `code_part.jinja`: Template for formatting code parts.
- `code_error.jinja`: Template for formatting code errors.
- `html_content.jinja`: Template for the overall HTML content.

## Example

Here is an example of how the HTML output might look:

```html
<h3>File: <a href="./path/to/file.py:10:5">path/to/file.py:10:5</a></h3>
<p>
  Error: <a href="https://docs.astral.sh/ruff/rules/#E123">E123</a> Some error
  message
</p>
<pre>
    | Some code part |
</pre>
```

## License

This project is licensed under the [MIT License](./LICENSE).
