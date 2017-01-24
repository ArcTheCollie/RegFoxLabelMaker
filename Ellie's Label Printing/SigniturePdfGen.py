import argparse
import csv
import codecs

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Frame, Paragraph
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys


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


NAME_STYLE = ParagraphStyle("Name", fontSize=12, allowWidows=3, allowOrphans=3)
INFO_STYLE = ParagraphStyle("Info", fontSize=8, leading=9, allowWidows=3, allowOrphans=3)
POST_STYLE = ParagraphStyle("POST", align=0, fontSize=8, leading=9, allowWidows=3, allowOrphans=3)


def truncate_further(text):
   fragments = text.split(" ")
   return " ".join(fragments[:-1])


def add_text_truncated(args, style=None, frame=None, canvas=None):
   text_to_add = args[:]
   while text_to_add:
      line = text_to_add.pop(0)
      line_was_added = False
      while not line_was_added:
         story = [Paragraph(line, style)]
         frame.addFromList(story, canvas)
         if len(story):
            line = truncate_further(line)
         else:
            line_was_added = True


def UnicodeDictReader(utf8_data, **kwargs):
   csv_reader = csv.DictReader(utf8_data, **kwargs)
   for row in csv_reader:
      yield {unicode(key, 'utf-8'):unicode(value, 'utf-8') for key, value in row.iteritems()}

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

   with codecs.open(csv_file, "r") as csv_file_object:
      data = list(UnicodeDictReader(csv_file_object))
      data.sort(key=lambda x: (x["lastname"].lower(), x["firstname"].lower()))

   c = canvas.Canvas(pdf_file, pagesize=letter)

   path_to_font = "C:\\Users\\Arc\\WorkSpace\\PycharmProjects\\FCLabelPrinter\\arial-unicode-ms.ttf"
   pdfmetrics.registerFont(TTFont('ArialMS', path_to_font))
   FONT_NAME = "ArialMS"  # TODO: Use TTFont to register Open Sans

   label_id = 0
   for row in data:
      if args.verbosity >= 1:
         print row[u"lastname"].encode("utf-8")
      x, y = Avery5260.bottom_left(label_id)
      c.setFont(FONT_NAME, 14)
      c.setStrokeColorRGB(0, 0, 0)
      if args.outlines:
         c.roundRect(x, y, Avery5260.LABEL_WIDTH, Avery5260.LABEL_HEIGHT,
                     0.125 * inch, stroke=1)

      sign_place_string = u"Signature _______________________"
      sign_fame = Frame(x, y,
                        Avery5260.LABEL_WIDTH,
                        Avery5260.LABEL_HEIGHT / 2,
                        leftPadding=0.125 * inch,
                        topPadding=0.125 * inch,
                        rightPadding=0.05 * inch,
                        bottomPadding=0,
                        showBoundary=0)
      add_text_truncated([sign_place_string], style=INFO_STYLE, frame=sign_fame, canvas=c)

      post_frame = Frame(x + Avery5260.LABEL_WIDTH - 0.2 * inch,
                         y,
                         0.2 * inch,
                         Avery5260.LABEL_HEIGHT / 4,
                         leftPadding=0,
                         topPadding=0,
                         rightPadding=0,
                         bottomPadding=0,
                         showBoundary=0)

      if int(row["postcard"]):
         add_text_truncated([u"P"], style=POST_STYLE, frame=post_frame, canvas=c)

      name_frame = Frame(x, y + Avery5260.LABEL_HEIGHT / 2,
                         Avery5260.LABEL_WIDTH / 2,
                         Avery5260.LABEL_HEIGHT / 2,
                         leftPadding=0.125 * inch,
                         topPadding=0.06 * inch,
                         rightPadding=0.125 * inch,
                         bottomPadding=0,
                         showBoundary=0)
      name = u"%s, %s" % (row["lastname"], row["firstname"])
      add_text_truncated([name], style=NAME_STYLE, frame=name_frame, canvas=c)

      info_frame = Frame(x + Avery5260.LABEL_WIDTH / 2,
                         y,
                         Avery5260.LABEL_WIDTH / 2,
                         Avery5260.LABEL_HEIGHT,
                         leftPadding=0.125 * inch,
                         topPadding=0.06 * inch,
                         rightPadding=0.125 * inch,
                         bottomPadding=0,
                         showBoundary=0)

      reg_attributes = ["#%s" % row["reg_id"], row["level"]]
      if int(row["is_minor"]):
            reg_attributes.append("Minor")
      reg_info = "\n".join(reg_attributes)
      add_text_truncated([reg_info], frame=info_frame, style=INFO_STYLE, canvas=c)
      label_id += 1
      if label_id % 30 == 0:
         c.showPage()
   if label_id % 30 != 0:
      c.showPage()
   c.save()


if __name__ == "__main__":
   main(sys.argv)
