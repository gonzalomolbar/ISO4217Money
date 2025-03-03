import os
from urllib import request

ISO4217_DOWNLOAD_URL = "https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml"
ISO4217_TABLE_PATH = os.path.join(
    os.path.dirname(__file__),
    "iso4217_money",
    "resources",
    "iso4217_currencies.xml",
)


def download_iso4217_currencies():
    response = request.urlopen(ISO4217_DOWNLOAD_URL)
    try:
        with open(ISO4217_TABLE_PATH, "wb") as f:
            f.write(response.read())
    finally:
        response.close()

    print(f"Downloaded ISO 4217 table to {ISO4217_TABLE_PATH}")


if __name__ == "__main__":
    download_iso4217_currencies()
