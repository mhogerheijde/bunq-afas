#!/usr/bin/env python3


"""
Converts bunq csv format into a format that Afas understands (ING currently)
"""

import csv
import locale
import math
import sys

def convert(infile, outfile):
    """
        Converts infile (in bunq CSV export format) into
        outfile (in ING csv export format)
    """
    csv.register_dialect(
        'ING',
        delimiter=',',
        quoting=csv.QUOTE_ALL,
        quotechar='"')

    input_csv = csv.DictReader(open(infile, newline=''))

    fieldnames = [
        "Datum",
        "Naam / Omschrijving",
        "Rekening",
        "Tegenrekening",
        "Code",
        "Af Bij",
        "Bedrag (EUR)",
        "MutatieSoort",
        "Mededelingen"
    ]
    writer = csv.DictWriter(open(outfile, 'w', newline=''), fieldnames=fieldnames, dialect='ING')

    writer.writeheader()
    for input_row in input_csv:

        # Input has the following columns
        # "Date","Amount","Account","Counterparty","Name","Description"

        amount = from_bunq(input_row["Amount"])
        af_bij = "Af" if (amount < 0) else "Bij"
        amount = to_ing(math.fabs(amount))

        writer.writerow({
            "Datum": input_row["Date"],
            "Naam / Omschrijving": input_row["Name"],
            "Rekening": input_row["Account"],
            "Tegenrekening": input_row["Counterparty"],
            "Code": "OV", # "Normal" money transfer at ING
            "Af Bij": af_bij,
            "Bedrag (EUR)": amount,
            "MutatieSoort": "Overschrijving", # "Normal" money transfer at ING
            "Mededelingen":  input_row["Description"],

        })



def from_bunq(amount):
    """
        Takes a stringf amount and converts to a floating using dot for decimal
        separator and comma for thousands separator
    """

    # To force , for thousands and . for decimals
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
    return locale.atof(amount)

def to_ing(amount):
    """Takes a floating number amount and converts to a string using comma for decimal separator"""

    # To force . for thousands and , for decimals
    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')
    return locale.format("%.2f", amount, grouping=False)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("usage: {1} input_file output_file".format(sys.argv[0]))
    else:
        convert(sys.argv[1], sys.argv[2])
