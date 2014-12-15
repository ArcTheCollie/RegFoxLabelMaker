import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import sys

FONT_NAME = "Open Sans"

def main(argv):
  if len(argv) < 3:
    print >> sys.stderr, "Usage: python fcreg/labels/pdfgen.py CSV_FILE PDF_FILE"
    sys.exit(2)
  _, csv_file, pdf_file = argv[:3]

  data = None
  with open(csv_file, "r") as csv_file_object:
    data = list(csv.DictReader(csv_file_object))
    data.sort(key=lambda x: x["fanname"])
    data.sort(key=lambda x: x["firstname"])
    data.sort(key=lambda x: x["lastname"])

  for row in data:
    print "Processing %s %s (%s)" % (row["firstname"], row["lastname"], row["fanname"])

  c = canvas.Canvas(pdf_file, pagesize=letter)
  c.drawString(100, 100, "Hello World")
  c.showPage()
  c.save()

if __name__ == "__main__":
  main(sys.argv)
