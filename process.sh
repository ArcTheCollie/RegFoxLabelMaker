#!/bin/bash
#
# Run the process. Format: process.sh INPUT_CSV [ADJUSTED_CSV [OUTPUT_PDF]]

set -eu

INPUT=${1:-registrations-FC2015-all-labels.csv}
ADJUSTED=${2:-${INPUT%.csv}-adjusted.csv}
OUTPUT=${3:-${INPUT%.csv}.pdf}

python -m fcreg.labels.csvadjuster $INPUT registrations-FC2015-all-labels-adjusted.csv
python -m fcreg.labels.pdfgen -v registrations-FC2015-all-labels-adjusted.csv registrations-FC2015-all-labels-adjusted.pdf
