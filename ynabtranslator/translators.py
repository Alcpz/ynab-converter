#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# File:  translators.py
# Author: Alberto Cabrera <Alberto.Cabrera@ull.edu.es>
#
# Date:  14/10/19
#

from abc import abstractmethod
from typing import List, Dict
# IngtoYnab
import xlrd


class PayeeTranslator(object):
  PAYEE_SEPARATOR = '|'

  @classmethod
  def load_file(cls, payee_filename: str) -> Dict:
    payees = {}
    with open(payee_filename, 'r') as payeefile:
      for line in payeefile:
        line = line.strip()
        if len(line) > 0 and line[0] != '#':
          payees[line.split(cls.PAYEE_SEPARATOR)[0]] = line.split(cls.PAYEE_SEPARATOR)[1]

    return payees


class RecordTranslator(object):
  """Generic class for  translation"""

  @classmethod
  @abstractmethod
  def transform(cls, records_in: List, payees_translator: Dict = {}) -> List:
    """Transform a List of records in the original format to the target format"""
    ...

  @classmethod
  @abstractmethod
  def extract(cls, filename: str) -> List:
    """Extracts the records from the filename as a List of records"""
    ...


class IngtoYnab(RecordTranslator):
  """Translator from ING Spain to a compatible YNAB CSV format"""
  ING_DATE = 0
  ING_PAYEE = 3
  ING_MEMO = 4
  ING_FLOW = 6

  YNAB_DATE = 0
  YNAB_PAYEE = 1
  YNAB_MEMO = 2
  YNAB_OUTFLOW = 3
  YNAB_INFLOW = 4


  @classmethod
  def transform(cls, records_in: List, payees_translator: Dict = {}) -> List:

    new_records = []
    for row in records_in:
      ynab_record = [row[cls.ING_DATE], row[cls.ING_PAYEE], row[cls.ING_MEMO], 0, 0]
      if row[cls.ING_PAYEE] in payees_translator:
        ynab_record[cls.YNAB_PAYEE] = payees_translator[row[cls.ING_PAYEE]]
      if float(row[cls.ING_FLOW]) < 0:
        ynab_record[cls.YNAB_OUTFLOW] = -float(row[cls.ING_FLOW])
      else:
        ynab_record[cls.YNAB_INFLOW] = float(row[cls.ING_FLOW])
      new_records.append(ynab_record)

    return new_records

  @classmethod
  def extract(cls, filename: str) -> List:
    workbook = xlrd.open_workbook(filename)
    data_sheet = workbook.sheet_by_index(0)
    records = []
    for row_index in range(6, data_sheet.nrows):
      date = xlrd.xldate_as_datetime(data_sheet.row_values(row_index)[0], workbook.datemode).strftime("%m/%d/%Y")
      records.append([date] + data_sheet.row_values(row_index)[1:])
    return records
