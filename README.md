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
| Python 3.12 or newer | Runs the scripts |
| [Go](https://go.dev/dl/) 1.25 or newer | One-time: compiles the SDK when you install it |
| [Git](https://git-scm.com/downloads) | One-time: lets `pip` download the SDK's source code |
| A TRUF.NETWORK private key | Identifies and signs transactions as "you" |
| The `system:network_writer` role on that key | Required to create streams — see [step 6](#6-get-a-private-key-and-request-access) |

Don't worry if Go and Git aren't installed yet — that's covered below. Steps below have separate instructions for Windows, macOS, and Linux wherever the commands differ.

---

## 1. Check your Python version

Open a terminal in this folder (`quick-create`) and run:

**Windows (PowerShell):**
```powershell
python --version
```

**macOS / Linux:**
```bash
python3 --version
```

You need `3.12` or higher. If it's older (or missing), install a newer Python from [python.org](https://python.org) first — on macOS you can also use `brew install python@3.12`, and on Linux your package manager (e.g. `sudo apt install python3.12`) usually has it.

> The rest of this guide uses `python` for simplicity. On macOS/Linux, use `python3` for any command below that isn't run inside an activated virtual environment (once the virtual environment from step 4 is active, `python` works correctly on every OS).

---

## 2. Install Go

The SDK this tool depends on is compiled from source the first time you install it, which requires Go. (macOS/Linux users in a hurry can skip this — see the note in [step 5](#5-install-the-sdk-and-dependencies).)

**Windows:**
1. Go to [go.dev/dl](https://go.dev/dl/) and download the Windows installer (`.msi`).
2. Run it, accepting the defaults.
3. Close and reopen your terminal so it picks up the new install.

**macOS:**
- Easiest: install [Homebrew](https://brew.sh) if you don't have it, then run `brew install go`.
- Or download the `.pkg` installer for macOS from [go.dev/dl](https://go.dev/dl/) and run it.

**Linux:**
- Use your package manager, e.g. `sudo apt install golang-go` (Debian/Ubuntu), `sudo dnf install golang` (Fedora), or `sudo pacman -S go` (Arch).
- Or download the tarball from [go.dev/dl](https://go.dev/dl/) and follow the [official Linux install instructions](https://go.dev/doc/install).

**Verify (all platforms):**

```bash
go version
```

You should see something like `go version go1.25.x ...`.

---

## 3. Install Git

`pip` needs Git to fetch the SDK's source code. (Not needed if you use the prebuilt-wheel shortcut in [step 5](#5-install-the-sdk-and-dependencies).)

**Windows:**
Download the installer from [git-scm.com/downloads](https://git-scm.com/downloads) and run it with defaults.

**macOS:**
Usually already installed. If not, running `git --version` will offer to install the Xcode Command Line Tools — accept that, or run `brew install git`.

**Linux:**
Use your package manager, e.g. `sudo apt install git` (Debian/Ubuntu), `sudo dnf install git` (Fedora), or `sudo pacman -S git` (Arch).

**Verify (all platforms):**

```bash
git --version
```

---

## 4. Set up a virtual environment (recommended)

A virtual environment keeps this project's dependencies separate from anything else on your computer. From inside the `quick-create` folder:

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

## 5. Install the SDK and dependencies

With your virtual environment active:

```bash
pip install -r requirements.txt
```

This downloads and compiles `trufnetwork-sdk-py` from source, which is why Go and Git are needed. It can take a minute or two the first time — that's normal.

> **macOS/Linux shortcut:** prebuilt wheels (no Go/Git required) are published on the [releases page](https://github.com/trufnetwork/sdk-py/releases/latest) for Linux (`*manylinux*.whl`) and macOS (`*macosx*.whl`). Download the one matching your OS, then run `pip install /path/to/the-file.whl` instead of the command above. There's no prebuilt wheel for Windows, so Windows users need Go + Git and the command above.

---

## 6. Get a private key and request access

You need a private key (a long hex string) to sign transactions. If you don't already have one, any standard Ethereum-style wallet (e.g. MetaMask) can generate one for you and let you export it.

> **⚠️ Keep it secret.** Anyone with your private key has full control of that wallet. Never share it, commit it to source control, or paste it into a chat. Treat `config.ini` (step 7) as sensitive once it's filled in.

---

## 7. Configure `config.ini`

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

- **`private_key`** — the key from step 6 (with or without a leading `0x`, either works).
- **`mainnet`** — `false` to use the test network (recommended while you're learning), `true` for the real network.
- **`name`** — any unique name you choose for your stream. This name determines the stream's ID, so **don't change it** between creating the stream and inserting records into it later.

Save the file.

---

## 8. Create your stream

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

## 9. Insert a record

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

## Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| `config.ini: wallet.private_key is required` | You haven't filled in `private_key` in `config.ini` yet. |
| `config.ini: stream.name is required` | You haven't filled in `name` in `config.ini` yet. |
| An error mentioning permissions/roles | Your key hasn't been granted the `system:network_writer` role — see step 6. |
| An error saying the stream already exists | You already ran `create_stream.py` with this `name`. Either pick a new `name` in `config.ini`, or skip straight to `insert_record.py` — the stream is already there. |
| `'go' is not recognized` (Windows) / `go: command not found` (macOS/Linux) — same for `git` | Close and reopen your terminal after installing Go/Git so it picks up the new install; re-verify with `go version` / `git --version`. |
| `pip install -r requirements.txt` fails while compiling | Double-check `go version` works in the same terminal you're running `pip` from. On macOS/Linux, consider the prebuilt-wheel shortcut in [step 5](#5-install-the-sdk-and-dependencies) instead. |
| `python: command not found` (macOS/Linux) | Use `python3` instead of `python` outside of an activated virtual environment — see the note in [step 1](#1-check-your-python-version). |
| Timeouts or connection errors | Check your internet connection and that `mainnet` in `config.ini` is set the way you expect. |

---

## Using this as sample code

Both scripts are intentionally short and documented inline — `create_stream.py` and `insert_record.py` are meant to double as minimal, copy-pasteable examples of using `trufnetwork-sdk-py` to deploy a stream and insert a record, if you want to build your own application later.
