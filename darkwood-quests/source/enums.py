"""The code -> name tables of silvermere's enums, read from silvermere-types' enums.rs, so the
converter writes codes the way an overlay names them."""
import os
import re
import sys
from pathlib import Path

if not os.environ.get('SILVERMERE_SRC'):
    sys.exit('set SILVERMERE_SRC to a silvermere checkout')
SRC = (Path(os.environ['SILVERMERE_SRC']) / 'crates/silvermere-types/src/enums.rs').read_text()


def table(name):
    m = re.search(r'\n    ' + re.escape(name) + r' \{\n(.*?)\n    \}\n', SRC, re.S)
    if not m:
        raise KeyError(name)
    return {int(c): v for v, c in re.findall(r'^\s+(\w+) = (\d+) =>', m[1], re.M)}


def name(enum, code):
    t = table(enum)
    code = int(code)
    return t[code] if code in t else {'Unknown': code}
