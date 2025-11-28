# Path Handling Notes
(Resolving path issues after moving `run_all.py` into `v1_generic_events/`)

## ✔ Background
This project was refactored so that the Proof-of-Concept code (v1) and the production-oriented blog integration code (v2) are kept separate.

As part of this change, `run_all.py` was moved into:

```
v1_generic_events/
```

This directory change introduced unexpected path resolution issues, especially for:

- font files (`./fonts/...`)
- output directories (`./output/...`)
- automated execution (cron, scheduled scripts, etc.)

The root cause was that several paths were defined as *relative paths*, which behave differently depending on **where Python is executed from (CWD)**.

---

## ✔ Key Points of the Path Issue

### 1. “Relative path” does **not** mean “relative to the script location”
The issue occurred because paths like `./fonts/...` were interpreted relative to the **current working directory**, not the directory containing the script.

Examples that produced different results:

```bash
cd project_root && python v1_generic_events/run_all.py
cd v1_generic_events && python run_all.py
```

→ In the first case, ./fonts pointed to project_root/fonts
→ In the second case, it pointed to v1_generic_events/fonts

This affected:

font loading

CSV/PDF output directory creation

file existence checks

2. The .env file intentionally uses a relative path (e.g. ./fonts/...)
The goal was to keep environment variables untouched (minimal changes).

3. Converting relative paths to absolute paths using BASE_DIR solves the issue
The correct approach is to:

detect where the script is located

construct all file paths relative to that location

This guarantees consistent behavior regardless of execution location or cron environment.

✔ Final Decision / Implementation Policy
1. Do not use FONTS_DIR
Reason:

The .env already contains FONT_PATH=./fonts/...

Duplicating the directory structure in both ENV and code is unnecessary

Minimal-change policy for v1

2. Do not use os.path.normpath
Not required for the current structure.
Can be reconsidered for v2 refactoring.

3. Keep the existing .env values unchanged
We continue to support:

```
FONT_PATH=./fonts/NotoSansJP-Regular.ttf
```

4. Convert the .env relative path into an absolute path using BASE_DIR

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REL_FONT_PATH = os.getenv("FONT_PATH")
FONT_PATH = os.path.join(BASE_DIR, REL_FONT_PATH)
```

This ensures:

consistent path behavior from any execution location

compatibility with cron / systemd / CI / Cloudflare Workers

safety for future containerized or remote deployments

✔ Future Considerations
Relative paths such as ./fonts/... may be treated as an anti-pattern
in automated or server-side environments where execution context varies.

A cleaner ENV structure may be adopted later, for example:

```
FONT_DIR=fonts
FONT_NAME=NotoSansJP-Regular.ttf
```

v2 (production-grade blog integration) will likely include a fully
redesigned folder and path structure, independent of v1 PoC constraints.