#!/usr/bin/env python3
"""
Insert a single record into the primitive stream defined in config.ini.

Reads the same config.ini as create_stream.py to determine the data
provider (derived from wallet.private_key) and the stream (stream.name).

Usage:
    python insert_record.py <value> [timestamp]

    value      Required. Numeric value to record (int or float).
    timestamp  Optional. Unix timestamp (seconds) for the record.
               Defaults to the current time if omitted.

On success, prints the stream ID, date, value, and transaction hash.
On failure, prints the error and exits with a non-zero status.

This file also serves as minimal sample code for writing to a primitive
stream with trufnetwork-sdk-py; the insert_record() call below is the
only part you need to lift into another application.
"""

import argparse
import sys
import time

from trufnetwork_sdk_py.client import TNClient
from trufnetwork_sdk_py.utils import generate_stream_id

from common import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("value", type=float, help="Value to record")
    parser.add_argument(
        "timestamp",
        type=int,
        nargs="?",
        default=None,
        help="Unix timestamp in seconds (default: now)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timestamp = args.timestamp if args.timestamp is not None else int(time.time())

    try:
        private_key, url, stream_name = load_config()

        client = TNClient(url, private_key)
        stream_id = generate_stream_id(stream_name)

        # wait=True (the default) blocks until the insert is confirmed on-chain,
        # so the tx_hash printed below is guaranteed valid once we get here.
        tx_hash = client.insert_record(stream_id, {"date": timestamp, "value": args.value})
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Stream ID: {stream_id}")
    print(f"Date: {timestamp}")
    print(f"Value: {args.value}")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    main()
