import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

import qrcode
from dotenv import load_dotenv


@dataclass
class WifiConfiguration:
    ssid: str
    password: str
    security: Literal["WPA", "WEP", "nopass"]
    hidden: Literal["true", "false"]


def load_configuration() -> WifiConfiguration:
    load_dotenv()

    ssid = os.getenv("WIFI_SSID", None)
    if ssid is None:
        raise ValueError("SSID is a required field")

    password = os.getenv("WIFI_PASSWORD", None)
    if password is None:
        raise ValueError("password is a required field")

    security = os.getenv("WIFI_SECURITY", "WPA")
    if security not in ["WPA", "WEP", "nopass"]:
        raise ValueError("security must be one of WPA, WEP or nopass")

    hidden = os.getenv("WIFI_HIDDEN", "false")
    if hidden not in ["true", "false"]:
        raise ValueError("hidden must be one of true, false")

    return WifiConfiguration(
        ssid=ssid,
        password=password,
        security=cast(Literal["WPA", "WEP", "nopass"], security),
        hidden=cast(Literal["true", "false"], hidden),
    )


def wifi_connection_string(wifi_configuration: WifiConfiguration) -> str:
    return (
        f"WIFI:T:{wifi_configuration.security};"
        f"S:{wifi_configuration.ssid};"
        f"P:{wifi_configuration.password};"
        f"H:{wifi_configuration.hidden};"
        f";"
    )


def generate_qr_code(wifi_configuration: WifiConfiguration):
    wifi_string = wifi_connection_string(wifi_configuration)

    # Generate QR code
    qr = qrcode.QRCode(
        version=None,  # automatic size
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )

    qr.add_data(wifi_string)
    qr.make(fit=True)

    output_file = Path(__file__).parent / f"{wifi_configuration.ssid}_qr_code.png"

    img = qr.make_image(fill_color="black", back_color="white")

    img.save(output_file)
    print(f"QR code saved to {output_file}")

    # Optional: show the QR code
    img.show()


if __name__ == "__main__":
    # Replace these values
    SSID = "MyWiFiNetwork"
    PASSWORD = "SuperSecretPassword"

    wifi_configuration = load_configuration()

    generate_qr_code(wifi_configuration)
