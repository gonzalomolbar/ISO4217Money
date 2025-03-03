import os
from datetime import date

import toml
from urllib import request
from xml.etree import ElementTree

ISO_4217_DOWNLOAD_URL = "https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml"
ISO_4217_TABLE_PATH = os.path.join(
    os.path.dirname(__file__),
    "iso4217_money",
    "resources",
    "iso_4217_currencies.xml",
)

PYPROJECT_PATH = os.path.join(os.path.dirname(__file__), "pyproject.toml")

VERSION_MAJOR = 0
VERSION_MINOR = 3


def download_iso_4217_currencies():
    response = request.urlopen(ISO_4217_DOWNLOAD_URL)
    try:
        with open(ISO_4217_TABLE_PATH, "wb") as f:
            f.write(response.read())
    finally:
        response.close()

    print(f"Downloaded ISO 4217 table to {ISO_4217_TABLE_PATH}")


def update_version():
    # Load the existing pyproject.toml
    pyproject = toml.load(PYPROJECT_PATH)

    # Get the patch version dynamically via the ISO
    with open(ISO_4217_TABLE_PATH, "r") as file:
        raw_xml = ElementTree.fromstring(file.read())
    published_date = date(*map(int, raw_xml.attrib["Pblshd"].split("-")))
    patch_version = published_date.strftime("%Y%m%d")

    # Construct the new version
    new_version = f"{VERSION_MAJOR}.{VERSION_MINOR}.{patch_version}"

    # Update the version in pyproject.toml
    pyproject["project"]["version"] = new_version

    # Write the changes back to pyproject.toml
    with open(PYPROJECT_PATH, "w") as file:
        toml.dump(pyproject, file)

    print(f"Set version to {new_version}")


if __name__ == "__main__":
    download_iso_4217_currencies()  # Download the ISO 4217 table
    # update_version()  # Update the version
