from bs4 import BeautifulSoup
import requests
import regex as re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from urllib.request import urlretrieve

r = requests.get('https://ucpd.berkeley.edu/alerts-log-news/daily-crime-log')
soup = BeautifulSoup(r.content, 'lxml')

pdf_links = []
for elem in soup.find_all('a'):
    link = elem.get('href')
    if type(link) == str:
        if '.pdf' in link:
            pdf_links.append(link)

def pdf2txt(url):
    """@Source: James Jung, https://github.com/jameswsj10/Calhacks6/blob/master/data_extraction/webscrape.py"""
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(url, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    i = 1
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        #print(i)
        interpreter.process_page(page)
        i = i + 1

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

dates = []

for link in pdf_links:
    date = re.search(r'files/(.*)\.pdf', link).group(1)
    formatted_date = date[0:2] + "-" + date[2:4] + "-" + date[4:]
    dates.append(formatted_date)

for link in pdf_links:
    print(pdf2txt(link))

