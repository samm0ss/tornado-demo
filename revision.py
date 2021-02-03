import os
import subprocess

REVISION = "UNKNOWN"
_ROOTDIR = os.path.abspath(os.path.join(__file__, ".."))

try:
    revision = \
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_ROOTDIR)
    REVISION = revision.decode("utf-8").strip()
except Exception:
    try:
        REVISION = \
            open(os.path.join(_ROOTDIR, "revision.txt"), "rt").read().strip()
    except Exception:
        pass
