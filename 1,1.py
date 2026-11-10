
"""Скрипт перевірки середовища розробки."""

import sys
import importlib


def check_python_version():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("ПОПЕРЕДЖЕННЯ: потрібна версія Python 3.10 або новіша!")
    else:
        print("Версія Python підходить ✓")


def check_package(package_name: str) -> bool:
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'невідома')
        print(f"  {package_name}: {version} ✓")
        return True
    except ImportError:
        print(f"  {package_name}: НЕ ВСТАНОВЛЕНО ✗")
        return False


def main():
    check_python_version()

    print("\nВстановлені пакети:")
    packages = ['django', 'flask']
    results = {pkg: check_package(pkg) for pkg in packages}

    installed = sum(results.values())
    missing = len(packages) - installed

    print("\nПідсумок:")
    print(f"Встановлено пакетів: {installed}")
    print(f"Відсутні пакети: {missing}")

    if missing > 0:
        missing_packages = [pkg for pkg in packages if not results[pkg]]
        print("Для встановлення виконайте:")
        print("pip install " + " ".join(missing_packages))
    else:
        print("Усі необхідні пакети встановлено!")


if __name__ == "__main__":
    main()
