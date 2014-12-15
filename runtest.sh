#!/bin/bash

set -eu

[[ -f test.pdf ]] && rm test.pdf
python fcreg/labels/pdfgen.py test.pdf
[[ -f test.pdf ]] || { echo "test.pdf does not exist" >&2; exit 2; }
