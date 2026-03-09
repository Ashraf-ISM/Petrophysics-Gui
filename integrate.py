"""Compatibility launcher.

The application is now structured under `src/petroanalysis`.
This file is kept so existing workflows (`python3 integrate.py`) continue to work.
"""

import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from petroanalysis.app.launcher import main


if __name__ == "__main__":
    raise SystemExit(main())
