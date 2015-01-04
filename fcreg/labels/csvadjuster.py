import argparse
import csv
import os
import sys

minors = set(["00-13", "14-17"])

def parse_level(reg_level):
  reg_level = reg_level.split(",")[0]
  if reg_level == "Volunteer Staff":
    return "Attending"
  return reg_level

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument("input_csv")
  parser.add_argument("output_csv")
  args = parser.parse_args()
  
  with open(args.input_csv, "r") as csv_file_object:
    reader = csv.reader(csv_file_object)
    writer = csv.writer(open(args.output_csv, "w"))
    header_row = next(reader)
    writer.writerow(["reg_id","lastname","firstname","fanname","level","is_staff","is_minor"])
    for row in reader:
      reg_id, lastname, firstname, fanname, level, is_staff, is_minor = row
      writer.writerow([
          reg_id, lastname, firstname, fanname, parse_level(level),
          "1" if is_staff == "Yes" else "0", "1" if is_minor in minors else "0"])

if __name__ == "__main__":
  main(sys.argv)