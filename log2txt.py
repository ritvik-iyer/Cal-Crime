from PyPDF2 import PdfFileReader
import os
import codecs
from glob import glob
from os import path
import re

def pdf2txt(pdf_file):
    reader = PdfFileReader(open(pdf_file, "rb"))
    text = ""
    for num in range(reader.getNumPages()):
        text += str(reader.getPage(num).extractText())
    return text

def write2txt(dates):
    for date in dates:
        pdf_filename = "{}.pdf".format(date)
        text = pdf2txt(pdf_filename)
        with codecs.open('{}.txt'.format(date), "w+", "utf-8") as file:
            file.write(text)
            file.close()
        os.remove(pdf_filename)

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))



if __name__ == "__main__":
    dates = []
    for filename in find_ext('.', 'pdf'):
        first_match = re.findall(r'\\(.*)', filename)[0]
        second_match = re.findall(r'(.*).pdf', first_match)[0]
        dates.append(second_match)
    write2txt(dates)
