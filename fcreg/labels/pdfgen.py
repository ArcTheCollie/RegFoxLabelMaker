import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import sys

def main(argv):
  if len(argv) < 3:
    print >> sys.stderr, "Usage: python fcreg/labels/pdfgen.py CSV_FILE PDF_FILE"
    sys.exit(2)
  _, csv_file, pdf_file = argv[:3]

  c = canvas.Canvas(pdf_file, pagesize=letter)
  c.showPage()
  c.save()

if __name__ == "__main__":
  main(sys.argv)
