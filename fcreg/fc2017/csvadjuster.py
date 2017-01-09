import argparse
import UnicodeCsv
import sys
import csv

minors = set(["13-14", "15-17"])

def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument("input_csv")
   parser.add_argument("output_csv")
   args = parser.parse_args()

   with open(args.input_csv, "rb") as csv_file_object:
      reader = UnicodeCsv.UnicodeReader(csv_file_object, delimiter=',')
      writer = UnicodeCsv.UnicodeWriter(open(args.output_csv, "w"))
      header_row = next(reader)
      writer.writerow([u"reg_id",u"lastname",u"firstname",u"line1",u"line2",u"level",u"is_minor"])
      reg_id = 1
      try:
         for row in reader:
            firstname, lastname, line1, line2, level, is_minor = row
            writer.writerow(
               [u"%04d" % reg_id, lastname, firstname, line1, line2, level,
                u"1" if is_minor in minors else u"0"])
            reg_id += 1
      except csv.Error, e:
         sys.exit('file %s, line %d: %s' % (args.input_csv, reader.line_num, e))


if __name__ == "__main__":
   main(sys.argv)