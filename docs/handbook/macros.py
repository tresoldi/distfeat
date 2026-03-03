"""
MkDocs macros for the distfeat handbook.

Provides template helpers for including tracked examples,
displaying version information, and rendering example metadata.
"""

from pathlib import Path


def _examples_dir() -> Path:
    """Return the absolute path to the examples directory."""
    return Path(__file__).resolve().parent / "examples"


def define_env(env):
    """Define macros available in Markdown templates."""

    @env.macro
    def version() -> str:
        """Return the current distfeat version string."""
        import distfeat

        return distfeat.__version__

    @env.macro
    def include_example(relative_path: str) -> str:
        """Include an example file's contents as a Python code block.

        Usage: {{ include_example("ch03_getting_started/run.py") }}
        """
        path = _examples_dir() / relative_path
        if not path.exists():
            return f"<!-- Example not found: {relative_path} -->"
        content = path.read_text(encoding="utf-8").rstrip()
        return f"```python\n{content}\n```"

    @env.macro
    def example_command(example_dir: str) -> str:
        """Include the command to run an example.

        Usage: {{ example_command("ch03_getting_started") }}
        """
        path = _examples_dir() / example_dir / "command.txt"
        if not path.exists():
            return f"<!-- Command not found: {example_dir} -->"
        content = path.read_text(encoding="utf-8").strip()
        return f"```bash\n{content}\n```"

    @env.macro
    def example_output(example_dir: str) -> str:
        """Include the captured output of an example.

        Usage: {{ example_output("ch03_getting_started") }}
        """
        path = _examples_dir() / example_dir / "output.txt"
        if not path.exists():
            return f"<!-- Output not found: {example_dir} -->"
        content = path.read_text(encoding="utf-8").rstrip()
        return f"```\n{content}\n```"

    @env.macro
    def last_verified(example_dir: str) -> str:
        """Return the last-verified metadata for an example.

        Usage: {{ last_verified("ch03_getting_started") }}
        """
        path = _examples_dir() / example_dir / "meta.txt"
        if not path.exists():
            return "not yet verified"
        content = path.read_text(encoding="utf-8").strip()
        return content
