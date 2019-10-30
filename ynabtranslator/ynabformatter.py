#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# File:  ynabformatter.py
# Author: Alberto Cabrera <Alberto.Cabrera@ull.edu.es>
#
# Date:  14/10/19
#
from typing import List
from ynabtranslator.translators import RecordTranslator
import csv


class YnabFormatter(object):
  """"""
  YNAB_HEADERS = ['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']

  def __init__(self, translator: RecordTranslator):
    self.translator = translator

  def _read_sheet(self, filename: str, payee_dict: str = None) -> List:
    """Extracts the records from the origin file"""
    records_orig = self.translator.extract(filename)
    return self.translator.transform(records_orig, payee_dict)

  def _save_csv(self, filename: str, records: List):
    """Saves the YNAB compatible format file"""
    with open(filename, 'w') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      csv_writer.writerow(self.YNAB_HEADERS)
      for record in records:
        csv_writer.writerow(record)

  def translate_file(self, origin: str, target: str, payee_dict: str = None):
    """Translates the origin file using the translator specified in the target file
    Optionally, you can translate payees using the payee_dict
    """
    records = self._read_sheet(origin, payee_dict)
    self._save_csv(target, records)


