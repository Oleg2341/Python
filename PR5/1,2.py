
"""Генератор requirements.txt з перевіркою залежностей."""

import subprocess
import sys
import json
import importlib.metadata
import re
import os


def get_installed_packages() -> list[dict]:
    """Повертає список встановлених пакетів з версіями."""
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=json'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Помилка отримання списку пакетів")
        return []

    packages = json.loads(result.stdout)
    return packages


def generate_requirements(packages: list[dict], filename: str = 'requirements.txt'):
    """Записує пакети у файл requirements.txt."""
    ignored = ['pip', 'setuptools', 'wheel']

    with open(filename, 'w', encoding='utf-8') as file:
        for pkg in packages:
            if pkg['name'].lower() not in ignored:
                file.write(pkg['name'] + '==' + pkg['version'] + '\n')


def verify_requirements(filename: str = 'requirements.txt') -> bool:
    """Перевіряє наявність усіх пакетів з requirements.txt."""
    if not os.path.exists(filename):
        print("Файл requirements.txt не знайдено")
        return False

    ok = True

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if '==' not in line:
                continue

            name, version = line.split('==', 1)
            name = name.strip()
            version = version.strip()

            try:
                installed_version = importlib.metadata.version(name)

                if installed_version == version:
                    print(f"  {name}: OK ✓")
                else:
                    print(f"  {name}: версія не збігається ✗")
                    ok = False

            except importlib.metadata.PackageNotFoundError:
                print(f"  {name}: НЕ ВСТАНОВЛЕНО ✗")
                ok = False

    return ok


def main():
    packages = get_installed_packages()
    print(f"Знайдено {len(packages)} встановлених пакетів\n")

    for pkg in packages[:10]:
        print(f"  {pkg['name']}=={pkg['version']}")

    if len(packages) > 10:
        print(f"  ... та ще {len(packages) - 10}")

    generate_requirements(packages)
    print("\nФайл requirements.txt створено")

    ok = verify_requirements()
    print(f"\nПеревірка залежностей: {'✓ Усе OK' if ok else '✗ Є розбіжності'}")


if __name__ == "__main__":
    main()
