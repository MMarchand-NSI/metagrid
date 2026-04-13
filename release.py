#!/usr/bin/env python3
"""
Script de publication d'une nouvelle version.
Usage: python release.py 1.2.3
"""
import subprocess
import sys


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Erreur (code {result.returncode})")
        sys.exit(result.returncode)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python release.py <version>  (ex: 1.2.3)")
        sys.exit(1)

    version = sys.argv[1].lstrip("v")
    tag = f"v{version}"

    # Vérifier qu'on est sur main et que tout est commité
    dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    if dirty:
        print("Le dépôt a des modifications non commitées. Abandonnée.")
        sys.exit(1)

    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if branch != "main":
        print(f"Vous n'êtes pas sur main (branche actuelle : {branch}). Abandonnée.")
        sys.exit(1)

    print(f"\nPublication de la version {tag}\n")
    run(["git", "tag", tag])
    run(["git", "push", "origin", tag])
    print(f"\nTag {tag} poussé. La GitHub Action prend le relais.")


if __name__ == "__main__":
    main()
