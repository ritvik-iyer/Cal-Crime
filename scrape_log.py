from bs4 import BeautifulSoup
import requests
import regex as re
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import codecs


def get_pdfs(soup):
    pdf_links = []
    for elem in soup.find_all('a'):
        link = elem.get('href')
        if type(link) == str:
            if '.pdf' in link:
                pdf_links.append(link)
    return pdf_links


def get_dates(pdf_links):
    dates = []
    for link in pdf_links:
        date = re.search(r'files/(.*)\.pdf', link).group(1)
        formatted_date = date[0:2] + "-" + date[2:4] + "-" + date[4:]
        dates.append(formatted_date)
    return dates

def download_pdfs(pdf_links):
    """"Make sure you have PDFMiner.six installed on your computer before you run this method"""
    for i in range(len(pdf_links)):
        new_request = requests.get(pdf_links[i], stream=True)
        with open("{}.pdf".format(dates[i]), 'wb') as pdf:
            for chunk in new_request.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

def pdf2txt(pdf_link):
    """@Source: https://github.com/jameswsj10/Calhacks6/blob/master/data_extraction/webscrape.py
        This is a helper method for write2txt"""
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(pdf_link, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

def write2txt(dates):
    for date in dates:
        pdf_filename = "{}.pdf".format(date)
        text = pdf2txt(pdf_filename)
        with codecs.open('{}.txt'.format(date), "w+", "utf-8") as file:
            file.write(text)
            file.close()
        os.remove(pdf_filename)


if __name__ == "__main__":
    r = requests.get('https://ucpd.berkeley.edu/alerts-log-news/daily-crime-log')
    soup = BeautifulSoup(r.content, 'lxml')
    pdf_links = get_pdfs(soup)
    clean_pdfs = sorted(pdf_links)[3:]
    dates = get_dates(clean_pdfs)
    download_pdfs(clean_pdfs)
    write2txt(dates)
