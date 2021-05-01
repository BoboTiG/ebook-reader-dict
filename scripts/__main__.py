import subprocess
import sys
import threading

FILES = {
    "ca-langs.py": "wikidict/lang/ca/langs.py",
    "en-form-of.py": "wikidict/lang/en/form_of.py",
    "en-langs.py": "wikidict/lang/en/langs.py",
    "en-places.py": "wikidict/lang/en/places.py",
    "es-langs.py": "wikidict/lang/es/langs.py",
    "es-campos-semanticos.py": "wikidict/lang/es/campos_semanticos.py",
    "fr-domain-templates.py": "wikidict/lang/fr/domain_templates.py",
    "fr-langs.py": "wikidict/lang/fr/langs.py",
    "fr-regions.py": "wikidict/lang/fr/regions.py",
    "pt-escopo.py": "wikidict/lang/pt/escopos.py",
    "pt-gramatica.py": "wikidict/lang/pt/gramatica.py",
    "pt-langs.py": "wikidict/lang/pt/langs.py",
}


def replace(file: str, data: str) -> bool:
    """Update contents in the file, even if there was no change."""
    with open(file) as fh:
        original_content = fh.read()

    start = original_content.find("# START")
    end = original_content.find("# END")
    if start == -1 or end == -1:
        return False

    new_content = f"{original_content[:start]}# START\n{data}{original_content[end:]}"
    with open(file, "w") as fh:
        fh.write(new_content)
    return True


def process_script(script: str, file: str) -> None:
    """Process one script."""
    data = subprocess.check_output(["python", f"scripts/{script}"], text=True)
    if replace(file, data):
        print(f"Processed {script} with success.", flush=True)
    else:
        print(f" !! Error processing {script}", flush=True)


def main():
    """Entry point."""
    threads = []

    for script, file in sorted(FILES.items()):
        th = threading.Thread(target=process_script, args=(script, file))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    print("\nFriendly reminder: run ./check.sh")


if __name__ == "__main__":
    sys.exit(main())
