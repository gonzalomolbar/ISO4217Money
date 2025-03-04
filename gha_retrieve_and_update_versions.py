import os
import toml
from datetime import date
from xml.etree import ElementTree
import requests

ISO4217_TABLE_PATH = os.path.join(
    os.path.dirname(__file__),
    "iso4217_money",
    "resources",
    "iso4217_currencies.xml",
)

PYPROJECT_PATH = os.path.join(os.path.dirname(__file__), "pyproject.toml")


def _write_to_github_env_file(key: str, value: str):
    print(f"Setting '{key}' to '{value}'")
    with open(os.environ["GITHUB_ENV"], "a") as myfile:
        myfile.write(f"{key}={value}\n")


def retrieve_and_update_versions():
    # Load the existing pyproject.toml
    pyproject = toml.load(PYPROJECT_PATH)

    # Get the patch version dynamically via the ISO
    with open(ISO4217_TABLE_PATH, "r") as file:
        raw_xml = ElementTree.fromstring(file.read())
    published_date = date(*map(int, raw_xml.attrib["Pblshd"].split("-")))
    new_patch_version = published_date.strftime("%Y%m%d")

    # Extract the current version
    current_version = pyproject["project"]["version"]

    # Get the latest version from PyPI
    response = requests.get("https://pypi.org/pypi/iso4217-money/json")
    pypi_version = response.json()["info"]["version"]

    # Check if the current version is the latest version
    if current_version != pypi_version:
        new_version = current_version  # We don't want to update the version if it's not the latest
        _write_to_github_env_file("IS_CURRENT_VERSION_UP_TO_DATE", "false")
        _write_to_github_env_file("UPDATE_PATCH_VERSION", "false")
        _write_to_github_env_file("PYPI_VERSION", pypi_version)
        _write_to_github_env_file("CURRENT_VERSION", current_version)
        _write_to_github_env_file("NEW_VERSION", new_version)
    else:
        current_major_version, current_minor_version, current_patch_version = (
            current_version.split(".")
        )
        # Check if the patch version has changed
        if current_patch_version != new_patch_version:
            new_version = (
                f"{current_major_version}.{current_minor_version}.{new_patch_version}"
            )
            pyproject["project"]["version"] = new_version

            # Write the changes back to pyproject.toml
            with open(PYPROJECT_PATH, "w") as file:
                toml.dump(pyproject, file)

            _write_to_github_env_file("IS_CURRENT_VERSION_UP_TO_DATE", "true")
            _write_to_github_env_file("UPDATE_PATCH_VERSION", "true")
            _write_to_github_env_file("PYPI_VERSION", pypi_version)
            _write_to_github_env_file("CURRENT_VERSION", current_version)
            _write_to_github_env_file("NEW_VERSION", new_version)
        else:
            new_version = current_version  # There's nothing to update
            _write_to_github_env_file("IS_CURRENT_VERSION_UP_TO_DATE", "true")
            _write_to_github_env_file("UPDATE_PATCH_VERSION", "false")
            _write_to_github_env_file("PYPI_VERSION", pypi_version)
            _write_to_github_env_file("CURRENT_VERSION", current_version)
            _write_to_github_env_file("NEW_VERSION", new_version)


if __name__ == "__main__":
    retrieve_and_update_versions()
