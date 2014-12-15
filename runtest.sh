#!/bin/bash

set -eu

[[ -f test.pdf ]] && rm test.pdf
python fcreg/labels/pdfgen.py test.csv test.pdf
[[ -f test.pdf ]] || { echo "Fail: test.pdf does not exist." >&2; exit 2; }
echo "Pass."
