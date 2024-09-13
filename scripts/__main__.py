import os
import subprocess
import sys
import threading
from pathlib import Path

# TODO: Use the official API after https://github.com/astral-sh/ruff/issues/659 is done
from ruff_api import FormatOptions, format_string

FILES = {
    "all-namespaces.py": "wikidict/namespaces.py",
    "ca-labels.py": "wikidict/lang/ca/labels.py",
    "ca-langs.py": "wikidict/lang/ca/langs.py",
    "da-langs.py": "wikidict/lang/da/langs.py",
    "de-abk.py": "wikidict/lang/de/abk.py",
    "de-langs.py": "wikidict/lang/de/langs.py",
    "de-lang_adjs.py": "wikidict/lang/de/lang_adjs.py",
    "en-form-of.py": "wikidict/lang/en/form_of.py",
    "el-aliases.py": "wikidict/lang/el/aliases.py",
    "el-labels.py": "wikidict/lang/el/labels.py",
    "el-langs.py": "wikidict/lang/el/langs.py",
    "en-labels.py": "wikidict/lang/en/labels.py",
    "en-langs.py": "wikidict/lang/en/langs.py",
    "en-places.py": "wikidict/lang/en/places.py",
    "es-langs.py": "wikidict/lang/es/langs.py",
    "es-campos-semanticos.py": "wikidict/lang/es/campos_semanticos.py",
    "fr-domain-templates.py": "wikidict/lang/fr/domain_templates.py",
    "fr-langs.py": "wikidict/lang/fr/langs.py",
    "fr-racines-arabes.py": "wikidict/lang/fr/racines_arabes.py",
    "fr-regions.py": "wikidict/lang/fr/regions.py",
    "fr-temps-geologiques.py": "wikidict/lang/fr/temps_geologiques.py",
    "it-codelangs.py": "wikidict/lang/it/codelangs.py",
    "it-langs.py": "wikidict/lang/it/langs.py",
    "no-langs.py": "wikidict/lang/no/langs.py",
    "pt-codelangs.py": "wikidict/lang/pt/codelangs.py",
    "pt-escopo.py": "wikidict/lang/pt/escopos.py",
    "pt-gramatica.py": "wikidict/lang/pt/gramatica.py",
    "pt-langs.py": "wikidict/lang/pt/langs.py",
}

# En error will be raised when the percentage of deletions from the new content
# compared to the original content is higher than this constant.
MAX_PERCENT_DELETIONS = 1 / 100


class MarkersNotFoundError(ValueError):
    def __str__(self) -> str:
        return "Markers not found."


class TooManyDeletionsError(ValueError):
    def __init__(self, old: int, new: int) -> None:
        self.old = old
        self.new = new

    def __str__(self) -> str:
        return f"Too many deletions ({self.new - self.old:,}), please check manually."


def replace(file: str, data: str) -> None:
    """Update contents in the file, even if there was no change."""
    path = Path(file)
    original_content = path.read_text()

    start_marker, end_marker = "# START", "# END"
    if (start := original_content.find(start_marker)) < 0 or (end := original_content.find(end_marker)) < 0:
        raise MarkersNotFoundError()

    new_content = f"{original_content[:start]}{start_marker}\n{data}{original_content[end:]}"
    new_content = format_string(__file__, new_content, options=FormatOptions(line_width=120))
    percent_deletions = 1 - len(new_content.splitlines()) / len(original_content.splitlines())
    if percent_deletions > MAX_PERCENT_DELETIONS:
        raise TooManyDeletionsError(len(original_content.splitlines()), len(new_content.splitlines()))

    path.write_text(new_content)


def process_script(script: str, file: str, errors: dict[str, str]) -> None:
    """Process one script."""
    try:
        replace(file, subprocess.check_output(["python", f"scripts/{script}"], text=True))
    except Exception as exc:
        errors[script] = str(exc)
    else:
        print(f"Processed {script} with success.", flush=True)


def set_output(errors: int) -> None:
    """It is very specific to GitHub Actions."""
    if "CI" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "ab") as fh:
            fh.write(f"errors={errors}\n".encode())


def main() -> int:
    """Entry point."""
    threads = []
    errors: dict[str, str] = {}

    for script, file in sorted(FILES.items()):
        th = threading.Thread(target=process_script, args=(script, file, errors))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    set_output(len(errors))

    if errors:
        for script, error in errors.items():
            print(f" !! {script}")
            print(error)
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
