#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pkg_resources
from collections import OrderedDict


def clean_requrements_for_production():
    """for new version of pip to avoid conflict"""
    re_pattern = "==\w+.+.+"
    dump_data = []
    with open("requirements/base.txt") as package_file:
        packages = package_file.read()
        packages = packages.splitlines()
        for package in packages:
            dump_data.append(package.split("==")[0])
    with open("requirements/base.txt", "w") as package_file:
        for package in dump_data:
            package_file.write(f"{package}\n")


def update_requirements():
    list_of_packages = [tuple(str(ws).split()) for ws in pkg_resources.working_set]
    all_packages = dict(sorted(list_of_packages, key=lambda x: (x[0].lower(), x)))
    packages_available = []
    with open("requirements/base.txt", "r") as package_file:
        for _package in package_file:
            packages_available.append(_package.replace("\n", ""))

    if len(all_packages.items()) > len(packages_available):
        with open("requirements/base.txt", "w") as package_file:
            for _package, _version in all_packages.items():
                package_file.write(f"{_package}\n")
        with open("requirements/dev.txt", "w") as package_file:
            for _package, _version in all_packages.items():
                package_file.write(f"{_package}=={_version}\n")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings.prod")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    update_requirements()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
