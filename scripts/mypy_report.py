"""Parse a mypy report into GitHub action annotations."""
import subprocess
from dataclasses import dataclass


@dataclass
class Line:
    """A parsed line of output from mypy."""

    file: str
    line: int
    message_type: str
    message: str
    code: str | None


def parse_line(line: str) -> Line:
    """Read and split a line into its constituent parts."""
    location, message_type, message = line.split(" ", 2)
    location: str
    message_type: str
    message: str
    code = None

    # Parse the fie name and line number
    file, line_number = location.removesuffix(":").replace("\\", "/").split(":")

    # Parse the error code from the message
    message_type = message_type.removesuffix(":")
    if message_type == "error":
        try:
            message, code = message.rsplit("[", 1)
            code = "[" + code
        except ValueError:
            pass

    return Line(file, int(line_number), message_type, message.strip(), code)


def parse_results(results: str) -> list[tuple[Line, list[Line]]]:
    """Read and group all lines from mypy output."""
    results = results.strip().splitlines()

    annotations = []
    for i in range(len(results)):
        line = parse_line(results[i])
        if line.message_type != "error":
            # Additional information or notes, not a root annotation
            continue

        notes = []
        i += 1
        try:
            while (next_line := parse_line(results[i])).message_type != "error":
                notes.append(next_line)
                i += 1
        except IndexError:
            pass

        annotations.append((line, notes))

    return annotations


def output_results(results: list[tuple[Line, list[Line]]]) -> None:
    """
    Format results for GitHub action annotations.

    Annotation format:
     https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-error-message
    """
    for line, notes in results:
        message = line.message
        if notes:
            message += "\n\nNotes:"
        for note in notes:
            message += f"\n{note.message}"

        message = message.replace("\n", "%0A")

        title = "mypy " + (line.code or "")
        print(f"::error file={line.file},line={line.line},title={title.strip()}::{message}")


if __name__ == "__main__":
    result = subprocess.run(["mypy", "patsy", "migrations", "--no-error-summary"], stdout=subprocess.PIPE)
    if result.returncode != 0:
        output_results(parse_results(result.stdout.decode("utf-8")))
    exit(result.returncode)
