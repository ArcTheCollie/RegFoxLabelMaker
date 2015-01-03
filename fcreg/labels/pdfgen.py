import argparse
import csv
import os
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Frame, Paragraph
from reportlab.pdfgen import canvas
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

NAME_STYLE = ParagraphStyle("Name", fontSize=12)
INFO_STYLE = ParagraphStyle("Info", fontSize=8, leading=9)
        
def main(argv):
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--barcode_format", default="{0}")
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
    
    barcode_value = args.barcode_format.format(row["reg_id"])
    barcode = code128.Code128(barcode_value, barWidth=0.50, barHeight=0.375 * inch, humanReadable=True)
    barcode.drawOn(c,
        x + Avery5260.LABEL_WIDTH - 0.125 * inch - barcode.width,
        y + Avery5260.LABEL_HEIGHT - 0.125 * inch - barcode.height)

    name_frame = Frame(x, y + Avery5260.LABEL_HEIGHT / 2,
        Avery5260.LABEL_WIDTH - barcode.width,
        Avery5260.LABEL_HEIGHT / 2,
        leftPadding=0.125 * inch,
        topPadding=0.125 * inch,
        rightPadding=0.125 * inch,
        bottomPadding=0,
        showBoundary=0)
    name = "%s, %s" % (row["lastname"], row["firstname"])
    name_frame.addFromList([Paragraph(name, NAME_STYLE)], c)

    info_frame = Frame(x, y,
        Avery5260.LABEL_WIDTH,
        0.125 * inch + 2 * 9,
        leftPadding=0.125 * inch,
        topPadding=0,
        rightPadding=0.125 * inch,
        bottomPadding=0.125 * inch,
        showBoundary=0)
    fan_info = row["fanname"] or "(no fan name)"
    reg_attributes = ["#%s" % row["reg_id"], row["level"]]
    if int(row["is_minor"]): reg_attributes.append("Minor")
    if int(row["is_staff"]): reg_attributes.append("Staff")
    reg_info = " / ".join(reg_attributes)
    info_frame.addFromList([Paragraph(fan_info, INFO_STYLE), Paragraph(reg_info, INFO_STYLE)], c)
    
    label_id += 1
    if label_id % 30 == 0:
      c.showPage()
  if label_id % 30 != 0:
    c.showPage()
  c.save()

if __name__ == "__main__":
  main(sys.argv)
