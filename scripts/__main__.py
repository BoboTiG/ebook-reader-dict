import os
import subprocess
import sys
import threading
from pathlib import Path

FILES = {
    "all-namespaces.py": "wikidict/namespaces.py",
    "ca-labels.py": "wikidict/lang/ca/labels.py",
    "ca-langs.py": "wikidict/lang/ca/langs.py",
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


def replace(file: str, data: str) -> bool:
    """Update contents in the file, even if there was no change."""
    path = Path(file)
    original_content = path.read_text()
    start = original_content.find("# START")
    end = original_content.find("# END")
    if start == -1 or end == -1:
        return False

    path.write_text(f"{original_content[:start]}# START\n{data}{original_content[end:]}")
    return True


def process_script(script: str, file: str, errors: dict[str, str]) -> None:
    """Process one script."""
    try:
        data = subprocess.check_output(["python", f"scripts/{script}"], text=True)
    except subprocess.CalledProcessError as exc:
        errors[script] = str(exc)
        return

    if replace(file, data):
        print(f"Processed {script} with success.", flush=True)
        return

    errors[script] = "Processing error"


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

    print("\nFriendly reminder: run ./check.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
