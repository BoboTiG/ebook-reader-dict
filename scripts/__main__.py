import subprocess
import sys

# Missing EN si_units
# Missing FR arabiser
FILES = {
    "ca-langs.py": ("wikidict/lang/ca/langs.py", "[CA] Update langs"),
    "en-form-of.py": ("wikidict/lang/en/form_of.py", "[EN] Update 'form of'"),
    "en-langs.py": ("wikidict/lang/en/langs.py", "[EN] Update langs"),
    "en-places.py": ("wikidict/lang/en/places.py", "[FR] Update places"),
    "es-langs.py": ("wikidict/lang/es/langs.py", "[ES] Update langs"),
    "fr-domain-templates.py": (
        "wikidict/lang/fr/domain_templates.py",
        "[FR] Update domain templates",
    ),
    "fr-langs.py": ("wikidict/lang/fr/langs.py", "[FR] Update langs"),
    "pt-gramatica.py": ("wikidict/lang/pt/gramatica.py", "[PT] Update gramática"),
    "pt-langs.py": ("wikidict/lang/pt/langs.py", "[PT] Update langs"),
}


def commit(file: str, message: str) -> None:
    """Commit changes."""
    subprocess.check_call(["git", "add", file])
    subprocess.check_call(["git", "commit", "-m", message])


def replace(file: str, data: str) -> bool:
    """Update contents in the file, even if there was no change.
    Return True if the update actually changed something.
    """
    with open(file) as fh:
        original_content = fh.read()

    start = original_content.find("# START")
    end = original_content.find("# END")
    new_content = f"{original_content[:start]}# START\n{data}{original_content[end:]}"

    with open(file, "w") as fh:
        fh.write(new_content)

    return original_content != new_content


def main():
    """Entry point."""
    for script, (file, commit_msg) in sorted(FILES.items()):
        print(f"Processing {script} ...", end=" ", flush=True)
        data = subprocess.check_output(["python", f"scripts/{script}"], text=True)
        if replace(file, data):
            commit(file, commit_msg)
        print("OK", flush=True)
        break


if __name__ == "__main__":
    sys.exit(main())
