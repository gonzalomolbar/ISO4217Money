import os
from xml.etree import ElementTree

from iso4217_money.types import ISO4217Currency

ISO_4217_TABLE_PATH = os.path.join(
    os.path.dirname(__file__),
    "iso4217_currencies.xml",
)


def get_iso_4217_currencies() -> list[ISO4217Currency]:
    """Get the ISO 4217 currencies from the XML file."""
    with open(ISO_4217_TABLE_PATH, "r") as f:
        raw_xml = ElementTree.fromstring(f.read())

    alphabetical_code_to_iso_4217_currency_map: dict[str, ISO4217Currency] = {}
    for node in raw_xml.findall("CcyTbl/CcyNtry"):

        def _get_text(element_name: str) -> str:
            element = node.find(element_name)
            if element is None or element.text is None:
                raise RuntimeError(
                    f"Element '{element_name}' not found in node '{_get_text('CtryNm')}'"
                )
            return element.text.strip()

        entity = _get_text("CcyNm")
        if entity == "No universal currency":
            continue

        alphabetical_code = _get_text("Ccy")
        numeric_code = _get_text("CcyNbr")
        minor_unit = _get_text("CcyMnrUnts")
        country_name = _get_text("CtryNm")

        try:
            iso_4217_currency = alphabetical_code_to_iso_4217_currency_map[
                alphabetical_code
            ]
        except KeyError:
            alphabetical_code_to_iso_4217_currency_map[alphabetical_code] = {
                "entity": _get_text("CcyNm"),
                "alphabetic_code": alphabetical_code,
                "numeric_code": numeric_code,
                "minor_unit": minor_unit,
                "country_names": {
                    country_name,
                },
            }
        else:
            if iso_4217_currency["entity"] != entity:
                raise RuntimeError(
                    f"Entity mismatch for currency '{alphabetical_code}': '{entity}' != '{iso_4217_currency['entity']}'"
                )
            if iso_4217_currency["alphabetic_code"] != alphabetical_code:
                raise RuntimeError(
                    f"Alphabetical code mismatch for currency '{entity}': '{alphabetical_code}' != '{iso_4217_currency['alphabetic_code']}'"
                )
            if iso_4217_currency["numeric_code"] != numeric_code:
                raise RuntimeError(
                    f"Numeric code mismatch for currency '{alphabetical_code}': '{numeric_code}' != '{iso_4217_currency['numeric_code']}'"
                )
            if iso_4217_currency["minor_unit"] != minor_unit:
                raise RuntimeError(
                    f"Minor unit mismatch for currency '{alphabetical_code}': '{minor_unit}' != '{iso_4217_currency['minor_unit']}'"
                )
            iso_4217_currency["country_names"].add(country_name)

    return sorted(
        (alphabetical_code_to_iso_4217_currency_map.values()),
        key=lambda iso_4217_currency: iso_4217_currency["alphabetic_code"],
    )
