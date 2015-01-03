import argparse
import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import sys

FONT_NAME = "Helvetica" # TODO: Use TTFont to register Open Sans

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
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--outlines", action="store_true")
  arg_parser.add_argument("-v", "--verbose", dest="verbosity", action="count")
  arg_parser.add_argument("source", metavar="CSV_FILE")
  arg_parser.add_argument("dest", metavar="PDF_FILE")
  args = arg_parser.parse_args()

  csv_file = args.source
  pdf_file = args.dest
  if args.verbosity >= 1:
    print "Outputting %s to %s." % (csv_file, pdf_file)

  data = None
  with open(csv_file, "r") as csv_file_object:
    data = list(csv.DictReader(csv_file_object))
    data.sort(key=lambda x: (x["lastname"], x["firstname"], x["fanname"]))

  c = canvas.Canvas(pdf_file, pagesize=letter)
  label_id = 0
  for row in data:
    if args.verbosity >= 1:
      print "Processing %s %s (%s)" % (row["firstname"], row["lastname"], row["fanname"])
    x, y = Avery5260.bottom_left(label_id)
    c.setFont(FONT_NAME, 14)
    c.setStrokeColorRGB(0, 0, 0)
    if args.outlines:
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
