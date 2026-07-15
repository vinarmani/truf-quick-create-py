#!/usr/bin/env python3
"""
Create a new primitive stream on TRUF.NETWORK from a config file.

Reads config.ini (same directory as this script) for:
  - wallet.private_key : signing key for the deploying account
  - network.mainnet    : true for mainnet, false for testnet
  - stream.name        : unique human-readable name for the stream

Usage:
    python create_stream.py

On success, prints the creator address and the new stream's ID.
On failure, prints the error and exits with a non-zero status.

See insert_record.py for the companion script that writes data points into
the stream created here.

This file also serves as minimal sample code for deploying a primitive
stream with trufnetwork-sdk-py; the deploy_stream() call below is the
only part you need to lift into another application.
"""

import sys

from trufnetwork_sdk_py.client import TNClient, STREAM_TYPE_PRIMITIVE
from trufnetwork_sdk_py.utils import generate_stream_id

from common import load_config


def main() -> None:
    try:
        private_key, url, stream_name = load_config()

        client = TNClient(url, private_key)
        stream_id = generate_stream_id(stream_name)

        # wait=True (the default) blocks until the deploy is confirmed on-chain,
        # so the values printed below are guaranteed valid once we get here.
        client.deploy_stream(stream_id, STREAM_TYPE_PRIMITIVE)

        creator_address = client.get_current_account()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Creator address: {creator_address}")
    print(f"Stream ID: {stream_id}")


if __name__ == "__main__":
    main()
