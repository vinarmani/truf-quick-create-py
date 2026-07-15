"""
Shared config.ini loading for create_stream.py and insert_record.py.

Both scripts operate on the same stream, identified by wallet.private_key
(which also determines the data provider address) and stream.name, so the
parsing/validation lives here once instead of being duplicated per script.
"""

import configparser
import os

MAINNET_URL = "https://gateway.mainnet.truf.network"
TESTNET_URL = "https://gateway.testnet.truf.network"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def load_config(path: str = CONFIG_PATH) -> tuple[str, str, str]:
    """Read and validate (private_key, url, stream_name) from an INI file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    parser = configparser.ConfigParser()
    parser.read(path)

    private_key = parser.get("wallet", "private_key", fallback="").strip()
    mainnet = parser.getboolean("network", "mainnet", fallback=False)
    stream_name = parser.get("stream", "name", fallback="").strip()

    if not private_key:
        raise ValueError("config.ini: wallet.private_key is required")
    if not stream_name:
        raise ValueError("config.ini: stream.name is required")

    url = MAINNET_URL if mainnet else TESTNET_URL
    return private_key, url, stream_name
