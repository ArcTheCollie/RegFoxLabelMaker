#!/bin/bash

set -eu

[[ -f "test.pdf" ]] && rm test.pdf
python -m fcreg.labels.pdfgen -v test.csv test.pdf
[[ -f test.pdf ]] || { echo "Fail: test.pdf does not exist." >&2; exit 2; }

[[ -f "test_with_outlines.pdf" ]] && rm test_with_outlines.pdf
python -m fcreg.labels.pdfgen --outlines -v test.csv test_with_outlines.pdf
[[ -f test_with_outlines.pdf ]] \
    || { echo "Fail: test_with_outlines.pdf does not exist." >&2; exit 2; }
echo "Pass."
