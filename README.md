# Quick Create — Getting Started

Two small command-line scripts for [TRUF.NETWORK](https://truf.network):

- **`create_stream.py`** — creates a new "primitive stream" (a time-series data feed).
- **`insert_record.py`** — adds one data point (a value, at a point in time) to that stream.

Both read their settings from a single file, `config.ini`, so you only have to type in your details once.

This guide assumes no prior coding experience beyond having Python already installed. Follow the steps in order.

---

## What you'll need before you start

| Requirement | Why |
|---|---|
| Python 3.12 | Runs the scripts. The recommended install method (a prebuilt wheel, see step 3) currently targets Python 3.12 specifically. |
| [Go](https://go.dev/dl/) 1.25+, [Git](https://git-scm.com/downloads), and (Linux only) `patchelf` | Only needed if you build the SDK from source instead of using the prebuilt wheel — required on Windows (no prebuilt wheel exists yet), or if no wheel matches your OS/architecture. See step 3. |
| A TRUF.NETWORK private key | Identifies and signs transactions as "you" |
| A wallet balance: **TRUF** on mainnet, or **TT** (test token) on testnet | Every transaction (creating a stream, inserting a record) pays a network fee in that network's token — see [Fee Reference](#fee-reference) |

Most macOS/Linux users won't need Go, Git, or `patchelf` at all — the recommended install path in step 3 skips them entirely. Steps below have separate instructions for Windows, macOS, and Linux wherever the commands differ.

---

## 1. Check your Python version

Open a terminal in this folder (`truf-quick-create-py`) and run:

**Windows (PowerShell):**
```powershell
python --version
```

**macOS / Linux:**
```bash
python3 --version
```

You need `3.12` or higher. If it's older (or missing), install a newer Python from [python.org](https://python.org) first — on macOS you can also use `brew install python@3.12`, and on Linux your package manager (e.g. `sudo apt install python3.12`) usually has it.

> The rest of this guide uses `python` for simplicity. On macOS/Linux, use `python3` for any command below that isn't run inside an activated virtual environment (once the virtual environment from step 2 is active, `python` works correctly on every OS).

---

## 2. Set up a virtual environment (recommended)

A virtual environment keeps this project's dependencies separate from anything else on your computer. From inside the `truf-quick-create-py` folder:

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt should now start with `(venv)`. Do this every time you open a new terminal to work on this project.

> **Windows note:** if activation fails with a message about "running scripts is disabled", run this once and try again: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 3. Install the SDK and dependencies

With your virtual environment active.

### Recommended: install the prebuilt wheel

Prebuilt wheels of `trufnetwork-sdk-py` are published on the [releases page](https://github.com/trufnetwork/sdk-py/releases/latest) — no Go, Git, or compiler required. Open that page and download the asset matching your OS and CPU architecture. For the current release, that's:

- **Linux (x86_64):** a file named like `trufnetwork_sdk_py-<version>-cp312-cp312-linux_x86_64.whl`
- **macOS (Apple Silicon):** a file named like `trufnetwork_sdk_py-<version>-cp312-cp312-macosx_11_0_arm64.whl`

(`cp312` means the wheel is built for Python 3.12 — the version this guide asks you to install in step 1. If you're on a different Python version, a different CPU architecture, or Windows, no matching wheel exists yet — use the source-build fallback below instead.)

Then install the file you downloaded:

```bash
pip install /path/to/the-downloaded-file.whl
```

That's it — skip ahead to [step 4](#4-get-a-private-key-and-request-access).

### Fallback: build from source (required on Windows)

There's no Windows wheel yet, so Windows users — and anyone on an OS/architecture without a matching wheel above — need to build the SDK from source instead. This compiles Go code, so it needs a few extra tools first.

**Install Go 1.25+:**

- **Windows:** go to [go.dev/dl](https://go.dev/dl/), download the Windows installer (`.msi`), run it accepting the defaults, then close and reopen your terminal so it picks up the new install.
- **macOS:** install [Homebrew](https://brew.sh) if you don't have it, then run `brew install go` — or download the `.pkg` installer from [go.dev/dl](https://go.dev/dl/).
- **Linux:** use your package manager, e.g. `sudo apt install golang-go` (Debian/Ubuntu), `sudo dnf install golang` (Fedora), or `sudo pacman -S go` (Arch) — or download the tarball from [go.dev/dl](https://go.dev/dl/) and follow the [official Linux install instructions](https://go.dev/doc/install).

Verify with `go version` — you should see something like `go version go1.25.x ...`.

**Install Git:**

- **Windows:** download the installer from [git-scm.com/downloads](https://git-scm.com/downloads) and run it with defaults.
- **macOS:** usually already installed. If not, running `git --version` will offer to install the Xcode Command Line Tools — accept that, or run `brew install git`.
- **Linux:** use your package manager, e.g. `sudo apt install git` (Debian/Ubuntu), `sudo dnf install git` (Fedora), or `sudo pacman -S git` (Arch).

Verify with `git --version`.

**Linux only — install `patchelf`:**

The source build's `gopy_build` step uses `patchelf` to fix up the compiled library's shared-library paths. Without it, the build fails partway through with `patchelf: not found`.

```bash
sudo apt install patchelf   # Debian/Ubuntu
sudo dnf install patchelf   # Fedora
sudo pacman -S patchelf     # Arch
```

**Then install the SDK:**

```bash
pip install -r requirements.txt
```

This downloads and compiles `trufnetwork-sdk-py` from source, which is why Go and Git (and, on Linux, `patchelf`) are needed. It can take a minute or two the first time — that's normal.

---

## 4. Get a private key

You need a private key (a long hex string) to sign transactions. If you don't already have one, any standard Ethereum-style wallet (e.g. MetaMask) can generate one for you and let you export it.

> **⚠️ Keep it secret.** Anyone with your private key has full control of that wallet. Never share it, commit it to source control, or paste it into a chat. Treat `config.ini` (step 5) as sensitive once it's filled in.

> **💰 Fund the wallet.** Both scripts submit transactions, and every transaction pays a network fee — so this wallet needs a balance before either script will succeed: **TRUF** if you're using mainnet, or **TT** (test token) if you're using testnet. Without it, `create_stream.py` and `insert_record.py` will fail (see [Troubleshooting](#troubleshooting)). For exact amounts, see [Fee Reference](#fee-reference).

---

## 5. Configure `config.ini`

This folder ships a template, `config.ini.example`, with no secrets in it. Make your own copy named `config.ini` — that's the file the scripts actually read, and it's gitignored so your private key never gets committed.

**Windows (PowerShell):**
```powershell
Copy-Item config.ini.example config.ini
```

**macOS / Linux:**
```bash
cp config.ini.example config.ini
```

Now open `config.ini` in this folder with any text editor (Notepad works fine) and fill in the blanks:

```ini
[wallet]
private_key = your-private-key-here

[network]
mainnet = false

[stream]
name = my-first-stream
```

- **`private_key`** — the key from step 4 (with or without a leading `0x`, either works).
- **`mainnet`** — `false` to use the test network (recommended while you're learning), `true` for the real network. This also determines which token your wallet needs a balance of: **TT** for `false` (testnet), **TRUF** for `true` (mainnet) — see step 4.
- **`name`** — any unique name you choose for your stream. This name determines the stream's ID, so **don't change it** between creating the stream and inserting records into it later.

Save the file.

---

## 6. Create your stream

> Reminder: this submits a transaction, so your wallet needs a balance of TRUF (mainnet) or TT (testnet) — see step 4 and [Fee Reference](#fee-reference) (100 TRUF/TT per stream).

Still in the terminal, with your virtual environment active (same command on every OS, since the active virtual environment's `python` is used):

```bash
python create_stream.py
```

If everything is set up correctly, you'll see something like:

```
Creator address: 0xabcdef8d8...
Stream ID: st1234567890abcdef1234567890abcdef
```

(The values above are just an example — your real address and stream ID will be different. The script always prints the complete, untruncated string; copy the whole thing if you need to use it elsewhere.)

That's it — your stream now exists on TRUF.NETWORK. You only need to run this once per stream; running it again with the same `name` in `config.ini` will fail because the stream already exists.

---

## 7. Insert a record

> Reminder: this also submits a transaction, so it too needs a wallet balance of TRUF (mainnet) or TT (testnet) — see step 4 and [Fee Reference](#fee-reference) (1 TRUF/TT per insert).

Now add a data point to the stream you just created:

```bash
python insert_record.py 42.5
```

This records the value `42.5` at the current time. You'll see:

```
Stream ID: st1234567890abcdef1234567890abcdef
Date: 1737000000
Value: 42.5
Transaction hash: 0x8f3a2b1c4...
```

(As above, this is an example — the script always prints the full, untruncated transaction hash, not a shortened version.)

### Using a specific timestamp

To record a value at a specific time instead of "now", pass a second argument — a Unix timestamp (whole seconds since 1970-01-01 UTC):

```bash
python insert_record.py 42.5 1737000000
```

You can run `insert_record.py` as many times as you like, with different values (and optionally different timestamps), to keep adding data to the same stream.

---

## Fee Reference

Every transaction these scripts submit costs a network fee, paid in the wallet's balance of TRUF (mainnet) or TT (testnet). As of this writing:

| Script | Action | Fee |
|---|---|---|
| `create_stream.py` | Create a stream (`create_streams`) | **100 TRUF / TT per stream** |
| `insert_record.py` | Insert a record (`insert_records`) | **1 TRUF / TT per transaction** (flat — each run of this script is one transaction) |

Notes:

- The fee amount is identical on both networks — only the token's name differs (TRUF on mainnet, TT on testnet); both use 18 decimals.
- There's no separate "gas" charge on top of this — the action fee shown above is the only per-transaction cost.
- The fee is paid to the network's block leader, not burned.

So, at minimum, fund the wallet with 100 TRUF/TT before [step 6](#6-create-your-stream), plus 1 TRUF/TT for every subsequent [step 7](#7-insert-a-record) call.

---

## Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| `config.ini: wallet.private_key is required` | You haven't filled in `private_key` in `config.ini` yet. |
| `config.ini: stream.name is required` | You haven't filled in `name` in `config.ini` yet. |
| An error mentioning permissions/roles | Your key hasn't been granted the `system:network_writer` role — see step 4. |
| An error mentioning insufficient funds/balance | Your wallet needs TRUF (mainnet) or TT (testnet) to pay the transaction fee — see [Fee Reference](#fee-reference) for exact amounts. Double-check `mainnet` in `config.ini` matches the network you actually funded. |
| An error saying the stream already exists | You already ran `create_stream.py` with this `name`. Either pick a new `name` in `config.ini`, or skip straight to `insert_record.py` — the stream is already there. |
| `patchelf: not found`, or the build fails at a `gopy_build` step (Linux) | You're on the source-build fallback in [step 3](#3-install-the-sdk-and-dependencies) and are missing `patchelf` — install it (e.g. `sudo apt install patchelf`) and re-run `pip install -r requirements.txt`. If you don't specifically need the source build, switching to the prebuilt wheel in step 3 avoids this entirely. |
| `'go' is not recognized` (Windows) / `go: command not found` (macOS/Linux) — same for `git` | Close and reopen your terminal after installing Go/Git so it picks up the new install; re-verify with `go version` / `git --version`. |
| `pip install -r requirements.txt` fails while compiling | Double-check `go version` works in the same terminal you're running `pip` from. Unless you specifically need the source build, switch to the prebuilt-wheel install in [step 3](#3-install-the-sdk-and-dependencies) instead. |
| `python: command not found` (macOS/Linux) | Use `python3` instead of `python` outside of an activated virtual environment — see the note in [step 1](#1-check-your-python-version). |
| Timeouts or connection errors | Check your internet connection and that `mainnet` in `config.ini` is set the way you expect. |

---

## Using this as sample code

Both scripts are intentionally short and documented inline — `create_stream.py` and `insert_record.py` are meant to double as minimal, copy-pasteable examples of using `trufnetwork-sdk-py` to deploy a stream and insert a record, if you want to build your own application later.
