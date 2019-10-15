#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# File:  ingxlstocsv.py
# Author: Alberto Cabrera <Alberto.Cabrera@ull.edu.es>
#
# Date:  14/10/19
#

import argparse
import os

try:
  from ynabtranslator.ynabformatter import YnabFormatter
  from ynabtranslator.translators import IngtoYnab, PayeeTranslator
except ImportError:
  import sys
  sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
  from ynabtranslator.ynabformatter import YnabFormatter
  from ynabtranslator.translators import IngtoYnab, PayeeTranslator



def parse_args():
  parser = argparse.ArgumentParser(description='Transform an ING Spain xls transaction file to a YNAB compatible CSV')
  parser.add_argument('files', metavar='PATH', type=str, nargs='+',
                      help='CSV files to transform')
  parser.add_argument('-p', '--payee-reference-file', metavar='PATH', type=str,
                      help='Payee equivalent file. ')
  return parser.parse_args()


def main():
  args = parse_args()
  payees = {}
  if args.payee_reference_file:
    payees = PayeeTranslator.load_file(args.payee_reference_file)
  for filename in args.files:
    y_conv = YnabFormatter(IngtoYnab)
    filename_csv = f"{os.path.splitext(os.path.basename(filename))[0]}.csv"
    y_conv.translate_file(filename, filename_csv, payees)


if __name__ == '__main__':
  main()
