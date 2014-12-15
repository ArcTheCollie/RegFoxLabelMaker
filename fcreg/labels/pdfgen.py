import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import sys

FONT_NAME = "Helvetica" # TODO: Use TTFont to register Open Sans
PRINT_OUTLINES = False

class Avery5260:
  MARGIN_TOP = 0.5 * inch
  MARGIN_BOTTOM = 0.5 * inch
  MARGIN_LEFT = 0.1875 * inch
  MARGIN_RIGHT = 0.1875 * inch
  SPACE_X = 0.125 * inch
  SPACE_Y = 0
  LABEL_WIDTH = 2.625 * inch
  LABEL_HEIGHT = 1 * inch

  @staticmethod
  def bottom_left(label_id):
    row = label_id % 10
    column = ((label_id - row) / 10) % 3
    return (Avery5260.MARGIN_LEFT + column * (Avery5260.LABEL_WIDTH + Avery5260.SPACE_X),
        Avery5260.MARGIN_BOTTOM + (9 - row) * (Avery5260.LABEL_HEIGHT + Avery5260.SPACE_Y))

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

  c = canvas.Canvas(pdf_file, pagesize=letter)
  label_id = 0
  for row in data:
    print "Processing %s %s (%s)" % (row["firstname"], row["lastname"], row["fanname"])
    x, y = Avery5260.bottom_left(label_id)
    c.setFont(FONT_NAME, 14)
    c.setStrokeColorRGB(0, 0, 0)
    if PRINT_OUTLINES:
      c.roundRect(x, y, Avery5260.LABEL_WIDTH, Avery5260.LABEL_HEIGHT,
          0.125 * inch, stroke=1)
    c.drawString(x, y, "%s, %s (%s)"
        % (row["lastname"], row["firstname"], row["fanname"]))
    label_id += 1
    if label_id % 30 == 0:
      c.showPage()
  if label_id % 30 != 0:
    c.showPage()
  c.save()

if __name__ == "__main__":
  main(sys.argv)
