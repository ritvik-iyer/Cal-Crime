from bs4 import BeautifulSoup
import requests
import regex as re
from PyPDF2 import PdfFileReader
import os
import codecs
import pandas as pd

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
    for i in range(len(pdf_links)):
        new_request = requests.get(pdf_links[i], stream=True)
        with open("{}.pdf".format(dates[i]), 'wb') as pdf:
            for chunk in new_request.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

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

def remove_files(dates):
    for date in dates:
        pdf_filename = "{}.pdf".format(date)
        os.remove(pdf_filename)

def count_cases(dates):
    counts = []
    for date in dates:
        txt_file = "{}.txt".format(date)
        file = open(txt_file, 'r')
        file_contents = file.read()
        all_cases = re.findall(r'Case #:(.*)Case', file_contents)
        try:
            all_cases.append(re.findall(r'Case #(.*)Print', file_contents)[0])
        except Exception as e:
            counts.append(len(all_cases))
            continue
        counts.append(len(all_cases))
    return counts

def case_frame(dates, counts):
    frame = pd.DataFrame({'date':dates, 'count':counts})
    return frame


if __name__ == "__main__":
    r = requests.get('https://ucpd.berkeley.edu/alerts-log-news/daily-crime-log')
    soup = BeautifulSoup(r.content, 'lxml')
    pdf_links = get_pdfs(soup)
    clean_pdfs = sorted(pdf_links)[3:]
    dates = get_dates(clean_pdfs)
    download_pdfs(clean_pdfs)
    write2txt(dates)
    counts = count_cases(dates)
    frame = case_frame(dates, counts)
    frame.to_csv('crime_counts.csv', index = False)
